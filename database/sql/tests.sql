--db size
select datname, pg_size_pretty(pg_database_size(datname))
from pg_database;

--table size
SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  AND nspname !~ '^pg_toast'
  ORDER BY pg_relation_size(C.oid) DESC;

--Tests
--A01: 3 misplays != strikeout
insert into bugged_games select game_id, 'A01' from
(select g.game_id from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count = 3 and end_condition != 2) as tg
ON CONFLICT DO NOTHING;
--4
--last check: 29.05.2022

--A02: Games with more than 3 strikes
insert into bugged_games select game_id, 'A02' from
(select g.game_id from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count > 3
order by 1) as tg
ON CONFLICT DO NOTHING;
--21
--last check: 29.05.2022

--A03: Clue giver = clue receiver
insert into bugged_games select game_id, 'A03' from(
--detrimental characters that act twice in a row are written wrongly (Contrarian, Genius, Panicky)
select distinct clues.game_id, detrimental_characters from clues join games g on clues.game_id = g.game_id
where clue_giver = clue_receiver order by 1) as gidc;
--2
--last check: 29.05.2022

--A04: Games missed during restructuring
select g.game_id from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is null and detrimental_characters is false;
--0
--last check: 29.05.2022

--A05: Difference in the number of actions between players per game should not be more than 1
insert into bugged_games select distinct game_id, 'A05'
-- select distinct game_id
-- select turns, player, game_id, diff
from (
    select turns, cpi.game_id, abs(turns - max(turns) OVER (PARTITION BY cpi.game_id)) as diff
    from (
        select count(*) as turns, player, game_id
        from (
            select turn_action, player, game_id
            from card_actions
            union all
            select turn_clued, clue_giver, game_id
            from clues
            ) as t
        where turn_action is not null
        group by player, game_id
        ) as cpi
    join games g on cpi.game_id = g.game_id
    where detrimental_characters is false
    group by turns, cpi.game_id, player
    ) as c
where diff > 1
order by game_id;
--35
--last check: 29.05.2022

--A06: One action per turn
select turn_action, game_id, count(*) from (
    select turn_action, game_id
    from card_actions
    union all
    select turn_clued, game_id
    from clues
    ) as t1
where turn_action is not null
group by turn_action, game_id
having count(*) > 1
order by game_id;
--0
--last check: 29.05.2022

--A07: Rank clues contain only numbers
select * from clues
where clue_type = 'ratio' and convert_to_int(clue) is null;
--0
--last check: 29.05.2022

CREATE OR REPLACE FUNCTION convert_to_int(v_input text)
RETURNS INTEGER AS $$
DECLARE v_int_value INTEGER DEFAULT NULL;
BEGIN
    BEGIN
        v_int_value := v_input::INTEGER;
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Invalid integer value: "%".  Returning NULL.', v_input;
        RETURN NULL;
    END;
RETURN v_int_value;
END;
$$ LANGUAGE plpgsql;

--A08: Delete detrimental characters
delete from card_actions where game_id in
(select game_id from games where detrimental_characters is true);

delete from clues where game_id in
(select game_id from games where detrimental_characters is true);
--ok
--last check: 29.05.2022

--A09: Unassigned actions
select * from card_actions where turn_action is not null and action_type is null;
select * from card_actions where turn_action is null and action_type is not null;
--0
--last check: 29.05.2022

--A10: Counts
select count(*) from games;
--771921
select count(*) from decks;
--5674956
select count(*) from game_actions;
--33899704
select count(*) from player_notes;
--904956
select count(*) from variants;
select * from variants order by variant_id desc;
--1901 (-5 deleted vars)
select count(*) from card_actions;
--39507269
select count(*) from clues;
--12897660
--last check: 29.05.2022

--A11: Missed games in clues table
select g.game_id from games g left outer join clues c on g.game_id = c.game_id
where c.game_id is null
  and detrimental_characters is false
  and g.game_id in (
    select distinct game_id
    from game_actions
    where action_type in (2, 3)
)
order by 1;
--0
--last check: 29.05.2022

--A12: Games without any actions
insert into bugged_games select game_id, 'A12' from (
select g.game_id from games g left outer join game_actions ga on g.game_id = ga.game_id
where ga.game_id is null
order by 1) as gggi
ON CONFLICT DO NOTHING;
--248
--last check: 29.05.2022

--A13: Games that have actions in original table which are missed in restructured one
select distinct game_id
from card_actions
where game_id in (
    select distinct game_id
    from game_actions
    where action_type in (0, 1)
)
group by game_id
having max(turn_drawn) = 0;
--0
--last check: 29.05.2022

--A14: Count of records in related tables
select count(*) from games;
--771921
select count(distinct game_id) from card_actions;
select (select count(*) from games where detrimental_characters is true) +
(select count(*) from games where detrimental_characters is false);
--771921
--last check: 29.05.2022

--A15: Games with one less card on which have slot 5
select * from slots s join games g on s.game_id = g.game_id
where one_less_card is true and slot = 5;
--0
--last check: 29.05.2022

--A16: Games containing more than 5 card movements per turn
select count(*), s.game_id, turn from slots s
join games g on s.game_id = g.game_id
where one_extra_card is false
and turn != 0
group by s.game_id, turn
having count(*) > 5;
--0
--last check: 29.05.2022

--A17: Outdated CardActions (don't run anymore)
select distinct game_id from card_actions where card_suit != lower(card_suit);
--0
--last check: 29.05.2022

--A18: manual checking for a single game from all tables
select * from games where game_id = 774770;
select * from card_actions where game_id = 714844 order by turn_action;
select * from clues where game_id = 714844 order by turn_clued;
select s.game_id, turn, player, card_suit, card_rank, slot
    from slots s join card_actions ca on s.game_id = ca.game_id and s.card_index = ca.card_index
where s.game_id = 714844 order by turn, player, slot;

--A19: display bugged games
select * from bugged_games;
select game_id, count(*) from bugged_games group by game_id
having count(*) > 1;
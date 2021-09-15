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
insert into bugged_games select game_id from
(select g.game_id from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count = 3 and end_condition != 2) as tg ;
--17847 - game_id
--not ok

--A02: Games with more than 3 strikes
select g.game_id, count, variant from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count > 3;
--0
--ok

--A03: Clue giver = clue receiver
insert into bugged_games select game_id from(
--detrimental characters that act twice in a row are written wrongly (Contrarian, Genius, Panicky)
select distinct clues.game_id, detrimental_characters from clues join games g on clues.game_id = g.game_id
where clue_giver = clue_receiver order by 1) as gidc;
--209806, 402059
--not ok

--A04: Games missed during restructuring
select g.game_id from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is null and detrimental_characters is false;
--0
--ok

--A05: Difference in the number of actions between players per game should not be more than 1
insert into bugged_games select distinct game_id
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
--35 shifted games
--not ok

--A06: One action per turn
select * from (
    select turn_action, game_id, count(*) as count from (
        select turn_action, game_id
        from card_actions
        union all
        select turn_clued, game_id
        from clues
        ) as t1
    where turn_action is not null
    group by turn_action, game_id) as t2
where count > 1
order by game_id;
--0
--ok

--A07: Rank clues contain only numbers
select * from clues
where clue_type = 'rank' and convert_to_int(clue) is null;
--0
--ok

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
--193017
delete from clues where game_id in
(select game_id from games where detrimental_characters is true);
--51285
--ok

--A09: Unassigned actions
select * from card_actions where turn_action is not null and action_type is null;
select * from card_actions where turn_action is null and action_type is not null;
--0
--ok

--A10: Counts. Date: 29.07.2021 11:10
select count(*) from games;
--589 285
select count(*) from decks;
--4 677 943
select count(*) from game_actions;
--25 733 714
select count(*) from player_notes;
--628 063
select count(*) from variants;
--1 781
select count(*) from card_actions;
--30 343 966
select count(*) from clues;
--9 414 667

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
--ok

--A12: Games without any actions
insert into bugged_games select game_id from (
select g.game_id from games g left outer join game_actions ga on g.game_id = ga.game_id
where ga.game_id is null
order by 1) as gggi;
--240

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
--ok

--A14: Count of records in related tables
--06.09.2021
select count(*) from games;
--613283
select count(distinct game_id) from game_actions;
--613040
select g.game_id from games g left join game_actions ga on g.game_id = ga.game_id
where ga.game_id is null order by 1;
--243
--ok
select count(distinct game_id) from card_actions;
select count(*) from games where detrimental_characters is false;
--609425
--ok
select count(distinct game_id) from slots;
--595382+16105=611487
select * from games g left join slots s on g.game_id = s.game_id
where s.game_id is null
  and all_or_nothing is false
  and card_cycle is false
  and detrimental_characters is false;
--ok

--A15: Games with one less card on which have slot 5
select * from slots s join games g on s.game_id = g.game_id
where one_less_card is true and slot = 5;
--ok

--A16: Games containing more than 5 card movements per turn
select count(*), s.game_id, turn from slots s
join games g on s.game_id = g.game_id
where one_extra_card is false
and turn != 0
group by s.game_id, turn
having count(*) > 5;
--ok

--A17: Outdated CardActions
select distinct game_id from card_actions where card_suit != lower(card_suit);
--ok

--A18: Latest games
select count(*) from games where game_id between 620000 and 627181;
--7181
--ok
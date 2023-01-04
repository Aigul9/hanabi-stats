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

--
select test, count(*) from bugged_games group by test order by test;
-- A01	4
-- A02	21
-- A03	2
-- A05	35
-- A12	248

--Tests
--A01: 3 misplays != strikeout
insert into bugged_games select game_id, 'A01' from
(select g.game_id from games g
    where end_condition != 2
    and exists (select 1 from card_actions ca
                where ca.game_id = g.game_id
                having count(*) filter (where action_type = 'misplay') = 3)) t
on conflict do nothing;
--4
--last check: 04.01.2023

select * from bugged_games where test = 'A01';

--A02: Games with more than 3 strikes
insert into bugged_games select game_id, 'A02' from
(select distinct ca.game_id from card_actions ca
group by ca.game_id
having count(*) filter (where action_type = 'misplay') > 3) t
on conflict do nothing;
--31
--last check: 04.01.2023

select * from bugged_games where test = 'A02' order by 1;

--A03: Clue giver = clue receiver
insert into bugged_games select game_id, 'A03' from(
--detrimental characters that act twice in a row are written wrongly (Contrarian, Genius, Panicky)
select distinct clues.game_id from clues
where clue_giver = clue_receiver order by 1) as gidc
on conflict do nothing;
--2
--last check: 04.01.2023

select * from bugged_games where test = 'A03';

--A04: Games missed during restructuring
select g.game_id from games g
where detrimental_characters is false
  and not exists(select 1 from card_actions ca where g.game_id = ca.game_id);
--0
--last check: 04.01.2023

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
order by game_id
ON CONFLICT DO NOTHING;
--35
--last check: 21.07.2022

--A06:

--A07: Rank clues contain only numbers
select * from clues
where clue_type = 'rank' and convert_to_int(clue) is null;
--0
--last check: 04.01.2023

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

--A08:

--A09: Unassigned actions
select * from card_actions where turn_action is not null and action_type is null;
select * from card_actions where turn_action is null and action_type is not null;
--0
--last check: 04.01.2023

--A10: Counts
select count(game_id) from games;
--893158
select count(seed) from decks;
--6567050
select count(game_id) from game_actions;
--39303600
--VACUUM (ANALYZE, VERBOSE, FULL) decks;
select count(game_id) from player_notes;
--1092985
select count(variant_id) from variants;
select * from variants order by variant_id desc;
--2025
select count(game_id) from card_actions;
--45720530
select count(game_id) from clues;
--14942151
--last check: 04.01.2023

select
  table_schema,
  table_name,
  count_rows(table_schema, table_name)
from information_schema.tables
where
  table_schema not in ('pg_catalog', 'information_schema')
  and table_type = 'BASE TABLE'
order by 3 desc;

create or replace function
count_rows(schema text, tablename text) returns integer
as
$body$
declare
  result integer;
  query varchar;
begin
  query := 'SELECT count(1) FROM ' || schema || '.' || tablename;
  execute query into result;
  return result;
end;
$body$
language plpgsql;

--A11: Missed games in clues table
select g.game_id from games g left outer join clues c on g.game_id = c.game_id
where c.game_id is null
  and detrimental_characters is false
  and exists (
      select 1 from game_actions ga
      where ga.game_id = c.game_id
        and action_type in (2, 3))
order by 1;
--0
--last check: 04.01.2023

--A12: Games without any actions
insert into bugged_games select game_id, 'A12' from (
select g.game_id from games g left outer join game_actions ga on g.game_id = ga.game_id
where ga.game_id is null
order by 1) as gggi
on conflict do nothing;
--248
--last check: 04.01.2023

select * from bugged_games where test = 'A12';

--A13: Games that have actions in original table which are missed in restructured one
select distinct g.game_id from game_actions ga
join games g on g.game_id = ga.game_id
where detrimental_characters is false
and action_type in (0, 1)
and not exists (select 1 from card_actions ca
where ga.game_id = ca.game_id
    and turn_drawn > 0);
--0
--last check: 04.01.2023

--A14:

--A15: Games with one less card on which have slot 5
select * from slots s join games g on s.game_id = g.game_id
where one_less_card is true and slot = 5;
--0
--last check: 04.01.2023

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


--A05, A06, A16
--сделать партиции

--Tests
--A01: 3 misplays != strikeout
select g.game_id, count, variant, end_condition from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count = 3 and end_condition != 2;
--17847 - game_id

--A02: Games with more than 3 strikes
select g.game_id, count, variant from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count > 3;

--A03: Clue giver = clue receiver
--detrimental characters that act twice in a row are written wrongly (Contrarian, Genius, Panicky)
select distinct clues.game_id, detrimental_characters from clues join games g on clues.game_id = g.game_id
where clue_giver = clue_receiver order by 1;

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
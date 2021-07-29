--Tests
--A01: 3 misplays != strikeout
select g.game_id, count, variant, end_condition from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count = 3 and end_condition != 2;
--17847 - game_id
--

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

--A04: Games missed during restructuring
select g.game_id from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is null;

--A05: Difference in the number of actions between players per game should not be more than 1
--select distinct game_id
select turns, player, game_id, diff
from (
    select turns, player, cpi.game_id, abs(turns - max(turns) OVER (PARTITION BY cpi.game_id)) as diff
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

--A06: Turns count
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

--A07: Rank clues contain only numbers
select * from clues
where clue_type = 'rank' and convert_to_int(clue) is null;

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
delete from card_actions
where game_id in
(select game_id from games where detrimental_characters is true);

delete from clues
where game_id in
(select game_id from games where detrimental_characters is true);

--A09:
select * from card_actions where turn_action is not null and action_type is null;
select * from card_actions where turn_action is null and action_type is not null;

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
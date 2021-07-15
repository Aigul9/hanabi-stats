-- value in list
select * from games where 'dmoneysozz' = any(players);
select * from games where starting_player is not null;
select * from games where one_less_card is true order by date_time_finished desc;
select * from games where deck_plays is not null;
select * from games where game_id = 2906;
-- *list
select distinct unnest(players) from games;

select distinct tags from games;

-- filter value in list
select * from (select distinct unnest(players) p from games) g where p like '%test%';
select distinct unnest(players) from games where variant_id is null order by 1;
select count(*) from games where variant_id is null;

select distinct variant_id, variant, min(date_time_started) as creation_date
from games group by variant_id, variant order by creation_date;

-- variant of the month
select variant, year, month, cnt as count
from (
    select *, max(cnt) over (partition by year, month) as max_count
    from (
        SELECT
               variant,
               extract(year from date_time_started) as year,
               extract(month from date_time_started) as month,
               count(*) cnt
        from games
        where speedrun is false
          and variant not in ('No Variant', 'Rainbow (6 Suits)', 'Black (6 Suits)', '6 Suits', 'Black (5 Suits)')
        group by variant, year, month
        ) as g
    ) t
where cnt = max_count
order by 2, 3;

update games set speedrun = true where game_id = 313563;

select distinct variant, variant_id from games order by variant_id;

select * from decks order by seed, card_index;
select distinct seed from decks;

select count(*) from game_actions;
--25 349 287

select count(*) from decks;
--4 628 043

select * from player_notes where game_id = 103429 and player = 'TimeHoodie';

-- delete from player_notes where 1 = 1;
-- delete from game_actions where 1 = 1;
-- delete from games where 1 = 1;

CREATE INDEX games_index_variant_id  ON games (variant);
CREATE INDEX games_index_seed        ON games (seed);

-- ALTER TABLE games ADD CONSTRAINT games_seed_fkey FOREIGN KEY (seed) REFERENCES decks (seed);

select * from games left join decks on games.seed = decks.seed;

ALTER TABLE games ADD COLUMN starting_player integer;

select distinct players from games;

ALTER TABLE games ADD COLUMN num_players integer;
ALTER TABLE games ADD COLUMN variant_id integer;
ALTER TABLE games ADD COLUMN timed boolean;
ALTER TABLE games ADD COLUMN time_base integer;
ALTER TABLE games ADD COLUMN time_per_turn integer;
ALTER TABLE games ADD COLUMN card_cycle boolean;
ALTER TABLE games ADD COLUMN deck_plays boolean;
ALTER TABLE games ADD COLUMN empty_clues boolean;
ALTER TABLE games ADD COLUMN one_extra_card boolean;
ALTER TABLE games ADD COLUMN one_less_card boolean;
ALTER TABLE games ADD COLUMN all_or_nothing boolean;
ALTER TABLE games ADD COLUMN detrimental_characters boolean;
ALTER TABLE games ADD COLUMN score integer;
ALTER TABLE games ADD COLUMN num_turns integer;
ALTER TABLE games ADD COLUMN end_condition integer;
ALTER TABLE games ADD COLUMN date_time_started timestamp;
ALTER TABLE games ADD COLUMN date_time_finished timestamp;
ALTER TABLE games ADD COLUMN num_games_on_this_seed integer;
ALTER TABLE games ADD COLUMN tags varchar;

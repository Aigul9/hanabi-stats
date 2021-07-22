-- value in list
select * from games where 'Pascool' = any(players);
select * from games where starting_player is not null;
select * from games where one_less_card is true order by date_time_finished desc;
select count(*) from games where deck_plays is not null;
select count(*) from games where deck_plays is null;
select count(*) from games where speedrun = 'false';
select count(*) from games;
select * from games where game_id = 592314;
select * from games where players[starting_player + 1] = 'Valetta6789' and num_players != 2 and speedrun is false
order by game_id;

select * from games;
select * from decks;
select * from game_actions;
select * from player_notes;
select * from variants;

select count(*) from games;
select count(*) from decks;
select count(*) from game_actions;
select count(*) from player_notes;
select count(*) from variants;

select * from games where one_less_card is true and all_or_nothing is true;
select * from games where one_extra_card is true and all_or_nothing is true;

select * from card_actions where game_id = 588364 order by turn_action;
select * from clues where game_id = 588364 order by turn_clued;
-- delete from card_actions where 1 = 1;
-- delete from clues where 1 = 1;
select distinct game_id from card_actions order by 1;
select distinct game_id from clues;
select count(game_id) from card_actions;
select count(game_id) from clues;
select count(distinct game_id) from card_actions;
select count(distinct game_id) from clues;
select * from card_actions ca left outer join clues cl on ca.game_id = cl.game_id;
select * from game_actions where game_id = 403351;
update variants set colors[6] = 'Black' where variant_id = 1425;
select distinct ca.game_id from card_actions ca join games g on g.game_id = ca.game_id
where 'Valetta6789' = any(players) and speedrun is false;
select * from variants v join games g on v.variant = g.variant where game_id = 403355;
select * from variants where 'Black Reversed' = any(suits);
select * from (select distinct unnest(suits) p from variants) g where p like '%everse%';
update variants set suits[array_length(suits, 1)] =
    replace(suits[array_length(suits, 1)], ' Reversed', '')
    where suits[array_length(suits, 1)] like '%everse%';
where exists (select * from (select distinct unnest(suits) p from variants g) as gp where p like '%everse%');

select replace('Black Reversed', ' Reversed', '');

select distinct variant, g.game_id from games g join card_actions ca on g.game_id = ca.game_id;

select * from card_actions where game_id = 593001;
select * from games g left join card_actions ca on g.game_id = ca.game_id where ca.game_id is null;
select * from games g where not exists (select game_id from card_actions);

select * from variants where variant = 'Ambiguous & Dark Pink (5 Suits)';
select suits from variants
where array_length(colors, 1) = 1 and
      ('Black' = any(colors) or 'Brown' = any(colors) or 'Pink' = any(colors));

-- *list
select distinct unnest(players) from games where deck_plays is null;
select count(*) from
(select distinct unnest(players) from games where deck_plays is null) c;

select distinct tags from games;

-- filter value in list
select * from (select distinct unnest(players) p from games) g where p like '%test%';
select distinct unnest(players) from games where variant_id is null order by 1;
select * from games where variant_id is null;

select distinct variant_id, variant, min(date_time_started) as creation_date
from games group by variant_id, variant order by creation_date;

-- variant of the month
select variant, year, month, cnt as count
from (
    select *, max(cnt) over (partition by year, month) as max_count
    from (
        select
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

--games per month
select
       extract(year from date_time_started) as year,
       extract(month from date_time_started) as month,
       count(*) count
from games
where speedrun is true
group by year, month
order by year, month;

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

CREATE INDEX decks_index_seed        ON decks (seed);
CREATE INDEX game_actions_index_game_id        ON game_actions (game_id);
CREATE INDEX variants_index_variant_id     ON variants (variant_id);
CREATE INDEX card_actions_index_game_id        ON card_actions (game_id);
CREATE INDEX card_actions_index_card_index       ON card_actions (card_index);

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

select * from games where game_id = 5564;
select * from decks where seed = 'p3v2s22';
select * from game_actions where game_id = 5191;

select max(game_id) from games;

select distinct time_base from games where speedrun is true;
select * from games where speedrun is true and time_base != 0;

create table variants (
    variant_id integer primary key,
    variant varchar(255),
    max_score integer
);

insert into variants
select distinct variant_id, variant, 0 from games;

delete from games where variant is null;

select * from variants;
select * from variants where max_score is null;

update variants set max_score =
case
    when variant = '3 Suits' then 3 * 5
    when variant = '4 Suits' then 4 * 5
    when variant = 'No Variant' then 5 * 5
    when variant = '6 Suits' then 6 * 5
    when variant = 'Dual-Color Mix' then 6 * 5
    when variant = 'Ambiguous Mix' then 6 * 5
    when variant = 'Ambiguous & Dual-Color' then 6 * 5
    else cast(substring(variant, '\d') as integer) * 5
end
where max_score is null;

CREATE EXTENSION IF NOT EXISTS tablefunc;

create view missing_scores as
select distinct g.variant, g.variant_id, num_players from games g
join variants v on g.variant_id = v.variant_id
group by g.variant, g.variant_id, num_players, max_score
having max(score) != max_score;

select * from missing_scores;

-- select * from crosstab(
--     $$select variant, num_players, count(num_players) from missing_scores
--         group by variant, num_players
--         order by variant$$
--     ) as ct(variant varchar, _2 int, _3 int, _4 int, _5 int, _6 int);

-- select * from crosstab(
-- $$
-- select * from (values
--     ('Alternating Clues & Black (5 Suits)', 5, 1),
--     ('Alternating Clues & Black (5 Suits)', 4, 1),
--     ('Alternating Clues & Black (6 Suits)', 2, 1),
--     ('Alternating Clues & Black (6 Suits)', 4, 1),
--     ('Alternating Clues & Black (6 Suits)', 6, 1)
-- ) as t (datetime, trace, value)
-- $$
-- ) as final_result (
--     unixdatetime text,
--     trace1 int,
--     trace2 int,
--     trace3 int,
--     trace4 int
-- );

ALTER TABLE games ADD CONSTRAINT games_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES variants (variant_id);

select * from variants;
select variant, suits, colors from variants order by variant_id;
select variant, suits, colors from variants where colors = '{}' order by 1;
select * from variants where variant like '%Decep%';
select * from variants where variant like '%-Ones%';
ALTER TABLE variants ADD COLUMN max_score_2p int;
ALTER TABLE variants ADD COLUMN max_score_3p int;
ALTER TABLE variants ADD COLUMN max_score_4p int;
ALTER TABLE variants ADD COLUMN max_score_5p int;
ALTER TABLE variants ADD COLUMN max_score_6p int;

ALTER TABLE variants ADD COLUMN suits varchar[];
ALTER TABLE variants ADD COLUMN special_rank int;
ALTER TABLE variants ADD COLUMN special_deceptive boolean;
ALTER TABLE variants ADD COLUMN special_all_clue_colors boolean;
ALTER TABLE variants ADD COLUMN special_all_clue_ranks boolean;
ALTER TABLE variants ADD COLUMN special_no_clue_colors boolean;
ALTER TABLE variants ADD COLUMN special_no_clue_ranks boolean;
ALTER TABLE variants ADD COLUMN colors varchar[];

update variants v set max_score_2p = (
    select max(score) from games g where g.variant_id = v.variant_id and g.num_players = 2
    )
where 1 = 1;

update variants v set max_score_3p = (
    select max(score) from games g where g.variant_id = v.variant_id and g.num_players = 3
    )
where 1 = 1;

update variants v set max_score_4p = (
    select max(score) from games g where g.variant_id = v.variant_id and g.num_players = 4
    )
where 1 = 1;

update variants v set max_score_5p = (
    select max(score) from games g where g.variant_id = v.variant_id and g.num_players = 5
    )
where 1 = 1;

update variants v set max_score_6p = (
    select max(score) from games g where g.variant_id = v.variant_id and g.num_players = 6
    )
where 1 = 1;

create view missing_scores as
select distinct variant,
                case
                    when max_score_2p = max_score then '+'
                    else ''
                end as _2p,
                case
                    when max_score_3p = max_score then '+'
                    else ''
                end as _3p,
                case
                    when max_score_4p = max_score then '+'
                    else ''
                end as _4p,
                case
                    when max_score_5p = max_score then '+'
                    else ''
                end as _5p,
                case
                    when max_score_6p = max_score then '+'
                    else ''
                end as _6p
from variants;

select * from missing_scores;

-- select * from missing_scores
-- where '+' in (_2p, _3p, _4p, _5p, _6p);

select * from missing_scores
where '' in (_2p, _3p, _4p, _5p, _6p);

--completed variants
select m.variant, variant_id from missing_scores m
join variants v on m.variant = v.variant
where _2p = '+' and _3p = '' and _4p = '+' and _5p = '+' and _6p = ''
order by m.variant;

--missing variants
select m.variant, variant_id from missing_scores m
join variants v on m.variant = v.variant
where _2p = '' and _3p = '' and _4p = '' and _5p = '' and _6p = ''
order by m.variant;

select m.variant, variant_id from missing_scores m
join variants v on m.variant = v.variant
where _4p = '' and v.max_score >= 25
order by m.variant;

--variants which nobody tried
select variant, variant_id from variants
where max_score_2p is null and max_score_3p is null and max_score_4p is null
  and max_score_5p is null and max_score_6p is null
order by variant;

--variants without max score
select extract(epoch from sum(num_games) * (
    select avg(date_time_finished - date_time_started) from games where speedrun is false
    )) / 3600 / 7 * 12 / 365 as months from (
select case
when num_games is null then 10
else num_games
end as num_games from
(select distinct variant, num_players from games g where 'Valetta6789' = any(players)
group by variant, num_players
having max(score) != (
    select max_score
    from variants v
    where v.variant = g.variant
)) tb1
right outer join
--number of games to get max score on a variant
(select g.variant, g.variant_id, count(*) / num_max_scores as num_games, count(*), num_max_scores from games g
    join
    (
        select variant, count(*) as num_max_scores from games g
        where score = (
            select max_score from variants v where v.variant_id = g.variant_id
            )
          and speedrun is false
        group by variant
) t on g.variant = t.variant
group by g.variant, g.variant_id, t.num_max_scores) tb2
on tb1.variant = tb2.variant) rt;


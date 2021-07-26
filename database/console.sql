--select by condition
select * from games where game_id = 40447;
select * from games where one_less_card is true and all_or_nothing is true;
select * from games where one_extra_card is true and all_or_nothing is true;
select max(game_id) from games;
select * from decks where seed = 'p3v2s22';
select * from game_actions where game_id = 5191;
select * from variants where variant_id = 13;
select variant, variant_id, suits, colors from variants order by variant_id;
select * from card_actions where game_id = 4200 order by turn_action;
-- select * from card_actions where game_id = 58515 order by card_index;
select * from clues where game_id = 4200 order by turn_clued;

--!!!
select distinct game_id from clues where clue_giver = clue_receiver order by 1;

--join
select v.variant_id, v.variant, v.suits, v.colors from variants v join games g on v.variant = g.variant
where game_id = 539725;
select distinct ca.game_id, variant from card_actions ca join games g on ca.game_id = g.game_id
where variant like '%&%';
select count(distinct g.game_id) from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is null;
select count(distinct g.game_id)  from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is not null;

--db restructure
select * from card_actions;
select concat('hanab.live/replay/', game_id, '#', turn_action) from card_actions ca
where player = 'Valetta6789'
and card_rank = 3
and card_suit in ('Yellow', 'Green')
and action_type = 'play'
order by 1;

--count
select count(*) from games;
select count(*) from decks;
select count(*) from game_actions;
select count(*) from player_notes;
select count(*) from variants;
select count(*) from card_actions;
select count(*) from clues;
select count(distinct game_id) from card_actions;
select count(distinct game_id) from clues;

--missing scores
--gotten scores for all player count
select * from missing_scores
where '+' in (max_2p, max_3p, max_4p, max_5p, max_6p);
--
select * from missing_scores
where '' in (max_2p, max_3p, max_4p, max_5p, max_6p);
--completed variants
select m.variant, m.variant_id from missing_scores m
join variants v on m.variant = v.variant
where max_2p = '+' and max_3p = '' and max_4p = '+' and max_5p = '+' and max_6p = ''
order by m.variant;
--missing variants
select m.variant, m.variant_id from missing_scores m
join variants v on m.variant = v.variant
where max_2p = '' and max_3p = '' and max_4p = '' and max_5p = '' and max_6p = ''
order by m.variant;
--virgin variants
select variant, variant_id from variants
where max_score_2p is null and max_score_3p is null and max_score_4p is null
  and max_score_5p is null and max_score_6p is null
order by variant;

--delete
--delete from table where 1 = 1;

--useful functions
--value in list
select * from games where 'Valetta6789' = any(players);
--*list
select distinct unnest(players) from games;
--filter values in list
select * from (select distinct unnest(players) p from games) g where p like '%test%';
--remove from array (array, element)
select array_remove(ARRAY[1, 2, 3], 2);
--array length (array, dimension)
select array_length(ARRAY[1, 2, 3], 1);
select replace('Black Reversed', ' Reversed', '');

--queries
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

--number of months to get all max scores
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

--update
update variants set suits[array_length(suits, 1)] =
    replace(suits[array_length(suits, 1)], ' Reversed', '');

update variants set colors[6] = 'Brown' where variant_id in (1430);

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

--create view
create view missing_scores as
select distinct variant,
                variant_id,
                case
                    when max_score_2p = max_score then '+'
                    else ''
                end as max_2p,
                case
                    when max_score_3p = max_score then '+'
                    else ''
                end as max_3p,
                case
                    when max_score_4p = max_score then '+'
                    else ''
                end as max_4p,
                case
                    when max_score_5p = max_score then '+'
                    else ''
                end as max_5p,
                case
                    when max_score_6p = max_score then '+'
                    else ''
                end as max_6p
from variants;

--select
select * from games;
select * from decks;
select * from game_actions;
select * from player_notes;
select * from variants;
select * from card_actions;
select * from clues;
select * from missing_scores;

--crosstab
--CREATE EXTENSION IF NOT EXISTS tablefunc;
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

--create indices
CREATE INDEX games_index_variant_id ON games (variant);
CREATE INDEX games_index_seed ON games (seed);
CREATE INDEX decks_index_seed ON decks (seed);
CREATE INDEX game_actions_index_game_id ON game_actions (game_id);
CREATE INDEX variants_index_variant_id ON variants (variant_id);
CREATE INDEX card_actions_index_game_id ON card_actions (game_id);
CREATE INDEX card_actions_index_card_index ON card_actions (card_index);

--modify tables
--games
ALTER TABLE games ADD COLUMN starting_player integer;
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

ALTER TABLE games ADD CONSTRAINT games_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES variants (variant_id);

--variants
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

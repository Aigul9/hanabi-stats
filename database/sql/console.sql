--select by condition
select * from games where game_id = 40447;
select * from games where one_less_card is true and all_or_nothing is true;
select * from games where one_extra_card is true and all_or_nothing is true;
select max(game_id) from games;

select * from game_actions where game_id = 5191;
select * from game_actions where action_type = 4;
select * from variants where variant_id = 9999;
select * from variants where variant like '%ever%';
select variant, variant_id, suits, colors from variants order by variant_id;

select distinct game_id from card_actions;
select count(distinct game_id) from card_actions;
select count(distinct game_id) from clues;
select count(*) from games where game_id >= 30000 and game_id <= 40000;
select count(distinct game_id) from card_actions where game_id >= 30000 and game_id <= 40000;

select * from card_actions where game_id = 54642 order by turn_action;
select * from clues where game_id = 54642 order by turn_clued;
update card_actions set action_type = 'play' where game_id = 410466 and turn_action = 44;

select * from decks where seed = (
    select seed from games where game_id = 403401
    );

--delete
--delete from table where 1 = 1;
-- delete from card_actions where game_id = 597969;
-- delete from clues where game_id = 597969;
-- delete from card_actions where game_id in (410466, 345883, 403401);
-- delete from clues where game_id in (410466, 345883, 403401);
-- delete from decks where seed = 'p2v83s80';
-- delete from variants where variant_id = 9999;

--games - number of misplays
select distinct ca.game_id, g.variant, count(*) as count from card_actions ca
join games g on ca.game_id = g.game_id
where action_type = 'misplay'
group by ca.game_id, g.variant
order by 3 desc, 1;

-- select * from card_actions where game_id = 58515 order by card_index;
select count(*) from games where detrimental_characters is true;

--join
select v.variant_id, v.variant, v.suits, v.colors from variants v join games g on v.variant = g.variant
where game_id = 31452;
select ca.game_id from card_actions ca join games g on g.game_id = ca.game_id
where variant like 'Duck%';
select distinct ca.game_id, variant from card_actions ca join games g on ca.game_id = g.game_id
where variant like '%&%';
select count(distinct g.game_id) from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is null;
select count(distinct g.game_id)  from games g left outer join card_actions ca on g.game_id = ca.game_id
where ca.game_id is not null;

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

update variants set colors[2] = 'Pink' where variant_id = 1355;

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

update card_actions set card_suit = replace(card_suit, ' Reversed', '')
where card_suit like '%everse%';


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
--     datetime text,
--     trace1 int,
--     trace2 int,
--     trace3 int,
--     trace4 int
-- );
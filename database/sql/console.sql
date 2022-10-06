--select by condition
select * from games where game_id = 630384;
select * from games where one_less_card is true and all_or_nothing is true;
select * from games where one_extra_card is true and all_or_nothing is true;
select * from games where all_or_nothing is true;
select * from players_list;
--16105
select distinct unnest(players), count(*) from games where all_or_nothing is true
group by unnest(players);
select * from games where detrimental_characters is true order by game_id;
select max(game_id) from games;

select * from game_actions where game_id = 622762;
select * from game_actions where action_type = 4;
select * from variants where variant_id = 9999;
select * from variants where variant like '%ever%';
select variant, variant_id, suits, colors from variants order by variant_id;
select * from card_actions where game_id = 624940 and card_suit = 'Blue';
select * from slots where game_id = 627446;

select distinct game_id from card_actions;
select count(distinct game_id) from card_actions;
select count(distinct game_id) from clues;

select s.card_index, turn, slot, card_suit, card_rank, player, turn_drawn, turn_action
from slots s join card_actions ca
    on s.game_id = ca.game_id and s.card_index = ca.card_index
where s.game_id = 622688
order by turn, card_index;

delete from slots where game_id = 0;
delete from slots where game_id in (
    select game_id
    from games
    where all_or_nothing is true
);

select * from slots where game_id = 622688 and card_index = 10;
select * from slots order by turn, card_index;
--delete from slots where 1 = 1;

select * from card_actions where game_id = 622688 order by turn_action;
select * from card_actions where game_id = 2907 order by card_index;
select * from clues where game_id = 599392 order by turn_clued;

select * from games where game_id > 36000 and starting_player != 0 order by 1;

select * from decks where seed = (
    select seed
    from games
    where game_id = 403401
);

select * from games
where players <@ ARRAY['aitch2', 'Lanvin']::varchar[]
and variant = 'White & Dark Null (5 Suits)';

select * from games where players <@ ARRAY['Lanvin', 'Valetta6789']::varchar[]
order by 1 desc;
select * from games where players <@ ARRAY['Fireheart', 'Valetta6789']::varchar[];

--delete
-- delete from table where 1 = 1;
--
-- delete from slots where game_id >= 712498;
-- delete from card_actions where game_id >= 712498;
-- delete from clues where game_id >= 712498;
-- delete from game_actions where game_id >= 712498;
-- delete from tags where game_id >= 712498;
-- delete from player_notes where game_id >= 712498;
-- delete from games where game_id >= 712498;
--
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
select count(*) from slots;
--54656134

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

update card_actions set card_suit = lower(card_suit) where game_id >= 60000
and game_id < 100000;

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

-- delete from slots where game_id >= 627000;
-- delete from card_actions where game_id >= 627000;
-- delete from clues where game_id >= 627000;
-- delete from game_actions where game_id >= 627000;
-- delete from player_notes where game_id >= 627000;
-- delete from decks where seed in (
--     select distinct seed from games where game_id >= 627000
--     );
-- delete from games where game_id >= 627000;

select * from decks;
select distinct d.seed from decks d join games g on d.seed = g.seed
where variant = 'No Variant'
and num_players = 3
and detrimental_characters is false
and end_condition = 1
order by 1;

select card_suit,
       card_rank,
       ca.card_index,
       player,
       turn_drawn,
       turn_action,
       action_type,
       ca.game_id
from card_actions ca join games g on ca.game_id = g.game_id
where g.seed = 'p3v0s1'
order by ca.game_id, card_index;

select distinct game_id from player_notes order by 1;

select * from players_list order by 1;

select player, count(*) as games from player_notes
where player in (select * from players_list)
group by player
order by 2 desc;

--rakxer's stats, see discord 18.12.2021 21:25
select date(date_time_finished), count(*) from games
group by date(date_time_finished)
order by 1;

select date(date_time_finished), max(game_id) from games
group by date(date_time_finished)
order by 1;

select * from games g join variants v on g.variant_id = v.variant_id
where 'jmrtz' = any(players) and 'micerang' = any(players)
and num_players = 2 and score = max_score order by score desc;

select * from games where 'ADrone' = any(players) and extract(hour from date_time_finished) = '14';

select max(game_id) from games;
select max(game_id) from card_actions;
select * from games where game_id = 662505;

select max(game_id) from games;
--678610
--678620

select * from clues where game_id = 678611;

select distinct game_id from clues where clue_type = 'ratio' order by 1;

-- delete from games where game_id >= 630613 and game_id <= 640000;
-- delete from card_actions where game_id >= 630613;
-- delete from clues where game_id >= 630613;
-- delete from game_actions where game_id >= 630613;
-- delete from slots where game_id >= 630613;
-- delete from player_notes where game_id >= 630613;

select * from games where game_id = 651857;
select * from card_actions where game_id = 651857;
select * from clues where game_id = 651857;
select * from game_actions where game_id = 630613;
select * from slots where game_id = 679403;
select * from player_notes where game_id = 679403;

-- delete from games where game_id = 630613;
-- delete from card_actions where game_id = 630613;
-- delete from clues where game_id = 630613;
-- delete from game_actions where game_id = 630613;
-- delete from slots where game_id = 630613;
-- delete from player_notes where game_id = 630613;

select g.game_id, count, variant from
              (select distinct game_id, count(*) as count from card_actions
              where action_type = 'misplay'
              group by game_id) t
join games g on t.game_id = g.game_id
where count > 3
order by 1;

select * from games where game_id = 712498;
select * from decks where seed = 'p2v1646s1';
select * from games where seed = 'p2v1646s1';
select * from card_actions where game_id = 712498;

update decks set seed = concat(seed, '_syn') where seed in
(select distinct seed from games where variant_id in (16461, 18081, 18121, 18161));
update games set seed = concat(seed, '_syn') where variant_id in (16461, 18081, 18121, 18161);

delete from decks where seed = 'p3v59s46';

select * from games where game_id = 712498;
select min(game_id) from games;
select * from tags;

select max(variant_id) from variants;
select * from variants where variant_id = 1816;

-- Odds And Evens (6 Suits) (#1646)
-- Odds And Evens (5 Suits) (#1808)
-- Odds And Evens (4 Suits) (#1812)
-- Odds And Evens (3 Suits) (#1816)

select * from variants where variant_id = 1;
select * from variants where variant_id = 1646;
insert into variants values(16461);
insert into variants values(18081);
insert into variants values(18121);
insert into variants values(18161);

delete from variants where variant_id in ('16461', '18081', '18121', '18161');

INSERT INTO variants
(variant_id,
 variant,
 max_score,
 suits,
 special_rank,
 special_deceptive,
 special_all_clue_colors,
 special_all_clue_ranks,
 special_no_clue_colors,
 special_no_clue_ranks,
 colors,
 eff_2p,
 eff_34p,
 eff_5p,
 eff_6p)
SELECT 18161,
       variant,
max_score,
suits,
special_rank,
special_deceptive,
special_all_clue_colors,
special_all_clue_ranks,
special_no_clue_colors,
special_no_clue_ranks,
colors,
eff_2p,
eff_34p,
eff_5p,
eff_6p
FROM variants WHERE variant_id = 1816;

update games set variant_id = 16461 where variant_id = 1646;
update games set variant_id = 18081 where variant_id = 1808;
update games set variant_id = 18121 where variant_id = 1812;
update games set variant_id = 18161 where variant_id = 1816;

UPDATE variants
SET
    variant = 'Odds And Evens (3 Suits)',
 max_score = 15,
 suits = subquery.suits,
 special_rank = subquery.special_rank,
 special_deceptive = subquery.special_deceptive,
 special_all_clue_colors = subquery.special_all_clue_colors,
 special_all_clue_ranks = subquery.special_all_clue_ranks,
 special_no_clue_colors = subquery.special_no_clue_colors,
 special_no_clue_ranks = subquery.special_no_clue_ranks,
 colors = subquery.colors,
 eff_2p = subquery.eff_2p,
 eff_34p = subquery.eff_34p,
 eff_5p = subquery.eff_5p,
 eff_6p = subquery.eff_6p
FROM (
         SELECT variant,
                max_score,
                suits,
                special_rank,
                special_deceptive,
                special_all_clue_colors,
                special_all_clue_ranks,
                special_no_clue_colors,
                special_no_clue_ranks,
                colors,
                eff_2p,
                eff_34p,
                eff_5p,
                eff_6p
         FROM variants
         where variant = '3 Suits'
     ) AS subquery
WHERE variant_id = 1816;

select * from variants where variant_id = 1816;

select * from tags order by 1;
delete from tags where game_id = 752506;

select * from players_list order by 1;

insert into players_list values ('DMoney');
insert into players_list values ('TimeHoodie');

select * from games where left(variant, 7) = 'Funnels'
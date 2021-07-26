--gotten scores for all player count
select * from missing_scores
where '+' in (max_2p, max_3p, max_4p, max_5p, max_6p);
--non-gotten scores
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
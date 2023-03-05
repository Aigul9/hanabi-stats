select
    'kimbifille' as player,
    extract(year from date_time_started) as year,
    TO_CHAR(
       TO_DATE (extract(month from date_time_started)::text, 'MM')
       , 'Month') as month,
    round(sum(extract(epoch from date_time_finished - date_time_started) / 3600)) as hours
from games
where 'kimbifille' = any(players)
group by 1, 2, 3
order by 2 desc, 3 desc;
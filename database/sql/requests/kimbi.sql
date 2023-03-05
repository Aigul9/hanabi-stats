select
    'kimbifille' as player,
    extract(year from date_time_started) as year,
    extract(month from date_time_started) as month,
    round(sum(extract(epoch from date_time_finished - date_time_started) / 3600)) as hours
from games
where 'kimbifille' = any(players)
group by 1, 2, 3
order by 2 desc, 3 desc;
--monthly degenerates
select unnest(players),
                (sum(extract(epoch from date_time_finished - date_time_started)) / 3600)::int
from games
where extract(year from date_time_finished) = 'cur_year'
and extract(month from date_time_finished) = 'cur_month'
group by 1
order by sum(extract(epoch from date_time_finished - date_time_started)) desc, 1
limit 10;
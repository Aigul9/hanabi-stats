--group time by months (top degenerates)
with dates as (
    select unnest(players)                                            as p,
           date_time_started                                          as s,
           date_time_finished                                         as f,
           date_time_finished - date_time_started                     as d,
           extract(epoch from date_time_finished - date_time_started) as total_diff,
           extract(year from date_time_started)                       as ys,
           extract(year from date_time_finished)                      as yf,
           extract(month from date_time_started)                      as ms,
           extract(month from date_time_finished)                     as mf
    from games
--     where speedrun is false
)
select player, year,
       TO_CHAR(
           TO_DATE (month::text, 'MM')
           , 'Month') as month,
       hours
from (
         select player, year, month, hours, rank() over (partition by year, month order by hours desc) as rank
         from (select p as player, ys as year, ms as month, (sum(time_in_sec) / 3600)::int as hours
               from (select p,
                            ys,
                            ms,
                            case
                                when ms != mf then
                                    extract(epoch from date_trunc('month', f) - s)
                                else total_diff
                                end as time_in_sec
                     from dates
                     union all
                     select p,
                            yf,
                            mf,
                            case
                                when ms != mf then
                                    extract(epoch from f - date_trunc('month', f))
                                else 0
                                end
                     from dates
                    ) un
-- where p
-- in
--       (
--        'Valetta6789',
--        'kimbifille',
--        'Lanvin'
-- --        'RaKXeR',
-- --        'Libster',
-- --        'NoMercy',
-- --        'florrat2',
-- --        'timotree'
--           )
               group by player, year, month
              ) t
     ) t_rank
-- where player = 'scharkbite';
where rank = 1
order by year, TO_DATE (month::text, 'MM'), hours desc;
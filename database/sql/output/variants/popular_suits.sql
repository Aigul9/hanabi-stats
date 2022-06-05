with total_suits as (
    select count(*) as count
    from (select unnest(suits)
          from games g
                   join variants v on v.variant_id = g.variant_id) t
)

select suit, count(*), round(count(*) * 100.0 / (select count from total_suits), 2) as "%"
from (
         select game_id, unnest(suits) as suit
         from games g
             join variants v on g.variant_id = v.variant_id
     ) t
group by suit
order by 2 desc;
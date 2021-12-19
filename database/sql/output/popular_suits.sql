select suit, count(*), round(count(*) * 100.0 / 3538973, 2)
from (
         select game_id, unnest(suits) as suit
         from games g
             join variants v on g.variant_id = v.variant_id
     ) t
group by suit
order by 2 desc;

select count(*)
from (select unnest(suits) from games g
join variants v on v.variant_id = g.variant_id) t;
--3 538 973
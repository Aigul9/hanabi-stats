--Number of teammates
select player, count(distinct p) as teammates
from (select player, unnest(players) p from games g join players_list pl
    on pl.player = any(players)) t
group by player
order by 2 desc, 1;
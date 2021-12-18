select player, round(wins * 100.0 / games, 2) as wr, wins, games
from (
         select player,
                count(*) filter (where score = max_score) as wins,
                count(*)                                  as games
         from players_list pl
                  join games g on player = any (players)
                  join variants v on g.variant_id = v.variant_id
         group by player
     ) t
order by 2 desc;


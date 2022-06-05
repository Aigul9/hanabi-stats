select player,
       teammate,
       round(wins * 100.0 / games, 2) as wr,
       wins,
       games
from (
         select distinct player,
                         unnest(players) teammate,
                         count(*) filter (where score = max_score) as wins,
                         count(*) as games
         from games g
                  join players_list pl on pl.player = any (players)
                  join variants v on g.variant_id = v.variant_id
         where speedrun is false
         and num_players != 2
    group by player, unnest(players)
     ) t
where games > 50
order by 1, 3 desc;
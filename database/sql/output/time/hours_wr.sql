select player,
       LPAD(hour::text, 2, '0') as hour,
       round(wins * 100.0 / games, 2) as wr,
       wins,
       games
from (
         select player,
                extract(hour from date_time_finished) as hour,
                count(*) filter (where score = max_score) as wins,
                count(*)                                  as games
         from players_list pl
                  join games g on player = any (players)
                  join variants v on g.variant_id = v.variant_id
         where speedrun is false
         and num_players != 2
         group by player, extract(hour from date_time_finished)
     ) t
order by 1, 2;
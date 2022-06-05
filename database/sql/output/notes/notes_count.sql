select player, round(notes * 1.0 / games, 2) as ratio, games, notes
from (
         select player,
                count(distinct t.game_id)          as games,
                count(*) filter (where note != '') as notes
         from (
                  select pn.game_id, player, unnest(notes) as note
                  from player_notes pn
                           join games g on pn.game_id = g.game_id
                  where speedrun is false
                    and player in (select * from players_list)
              ) t
         group by player
     ) t1
order by 2 desc;
--player who bombed out the game
select t1.player,
       round("third strikes" * 100.0 / count, 2),
       "third strikes",
       count as "total games"
from (select player, count(*) as "third strikes"
from (select player,
             ca.game_id,
             action_type,
             rank() over (partition by ca.game_id order by turn_action desc) as rank
      from card_actions ca
               join games g on ca.game_id = g.game_id
      where end_condition = 2
        and speedrun is false
        and num_players != 2
        and action_type = 'misplay'
     ) t
where rank = 1
and player in (select player from players_list)
group by player) t1
join
(select player, count(*) as count from players_list pl join games
    on player = any(players)
    where num_players != 2
       and end_condition = 2
      and speedrun is false
    group by player) t2
on t1.player = t2.player
order by 2 desc;
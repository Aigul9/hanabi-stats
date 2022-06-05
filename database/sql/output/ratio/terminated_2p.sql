--number of terminated games for any pair of players which has more than 100 games
with pair
    as (select pl1.player as player1,
               pl2.player as player2
        from players_list pl1,
             players_list pl2
        --remove duplicates
        where pl1.player < pl2.player
    )
select player1,
       player2,
       total,
       term as terminated,
       round(term * 100.0 / total, 2) as "%"
from (select player1,
             player2,
             count(*)                                  as total,
             --terminated games
             count(*) filter (where end_condition = 4) as term
      from pair p
               join games g
                    on p.player1 = any (players)
                        and p.player2 = any (players)
      where num_players = 2
        and speedrun is false
      group by player1, player2
     ) t
where total >= 100
order by 5 desc;
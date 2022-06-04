--winning streak (state = 1) / losing streak (state = 0)
select player, count, start_game_id
from (select player, rank() over (partition by player order by count desc) as rank, count, start_game_id
      from (select player, min(game_id) as start_game_id, grp, count(*) as count
            from (select *,
                         row_number() over (partition by player order by game_id) -
                         row_number() over (partition by player, state order by game_id) as grp
                  from (select game_id,
                               unnest(players) as player,
                               score,
                               max_score,
                               seed,
                               case
                                   when score = max_score then 1
                                   else 0
                                   end         as state
                        from games g
                                 join variants v on g.variant_id = v.variant_id
                            and speedrun is false
                       ) t1
                 ) t2
      where state = 1
--       where state = 0
              and player in (select player from players_list)
            group by player, grp) t3
     ) t4
where rank = 1
order by 2 desc, 1;
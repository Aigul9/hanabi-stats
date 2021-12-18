--clean games
with players as (
    select player, count(*) as count from players_list pl join games
    on player = any(players)
    where num_players != 2
      and end_condition = 1
      and detrimental_characters is false
      and speedrun is false
      and all_or_nothing is false
      and one_extra_card is false
      and one_less_card is false
    group by player
)
select t1.player,
       round(t1.count * 1.0 / p.count, 2) as ratio,
       t1.count as count_clean,
       p.count as count_total
from (select pl.player, count(*) as count
      from (select *
            from games
            where num_players != 2
              and end_condition = 1
              and detrimental_characters is false
              and speedrun is false
              and all_or_nothing is false
              and one_extra_card is false
              and one_less_card is false
              and 'misplay' not in (
                select distinct action_type
                from card_actions
                where game_id = games.game_id
                  and action_type is not null
            )) t
               join players_list pl on pl.player = any (players)
      group by pl.player
     ) t1
join players p on t1.player = p.player
order by 2 desc, 1;
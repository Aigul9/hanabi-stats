--list of games and bdrs for all players (only normal and strikeout games)
with game_id_ as (
    select distinct game_id, variant
    from (select game_id, variant, unnest(players) as player
          from games
          where num_players != 2
            and speedrun is false
            and detrimental_characters is false
            and end_condition in (1, 2)
         ) t1
    where player in (select player from players_list)
)
--select pl.player, gi.game_id, gi.variant, coalesce(bdr_null, 0) as bdr
select pl.player, t.game_id, t.variant, bdr_null as bdr
from (
         select gi.game_id, gi.variant, count(*) as bdr_null
         from card_actions ca1
                  join game_id_ gi on ca1.game_id = gi.game_id
         where ca1.game_id = gi.game_id
           and ca1.action_type in ('discard', 'misplay')
           and ca1.card_rank not in (1, 5)
           and ca1.card_suit not in ('black', 'cocoa rainbow', 'gray pink')
           and ca1.card_suit not like 'dark%'
           and concat(card_suit, card_rank) not in (
             select concat(card_suit, card_rank)
             from card_actions ca2
             where ca2.game_id = gi.game_id
               and ca2.turn_drawn < ca1.turn_action
               and ca1.card_index != ca2.card_index
         )
         group by gi.game_id, gi.variant
     ) t
--right join game_id_ gi on t.game_id = gi.game_id
--join games g on g.game_id = gi.game_id
join games g on g.game_id = t.game_id
join players_list pl on pl.player = any(g.players)
where bdr_null > 2
order by pl.player, bdr desc, t.game_id;
--games and bdrs by player
with game_id_ as (
    select distinct game_id, variant
    from games
    where num_players
        != 2
      and speedrun is false
      and detrimental_characters is false
      and end_condition in (1, 2)
      and 'player_name' = any (players)
)
select 'player_name', gi.game_id, gi.variant, coalesce(bdr_null, 0) as bdr
from (
         select gi.game_id, gi.variant, count(*) as bdr_null
         from card_actions ca1
                  join game_id_ gi on ca1.game_id = gi.game_id
         where ca1.game_id = gi.game_id
           and ca1.action_type in ('discard', 'misplay')
           and ca1.card_rank not in (1, 5, 7)
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
right join game_id_ gi on t.game_id = gi.game_id
order by bdr desc, gi.game_id;
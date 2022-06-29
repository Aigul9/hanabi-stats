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

--distribution
with game_id_ as (
    select distinct game_id
    from (select game_id, unnest(players) as player
          from games
          where num_players != 2
            and speedrun is false
            and detrimental_characters is false
            and end_condition in (1, 2)
         ) t1
    where player in (select player from players_list)
)
select pl.player,
       max(bdr_null) as max_bdr,
       round(sum(case when coalesce(bdr_null, 0) = 0 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "0 bdr",
       round(sum(case when bdr_null = 1 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "1 bdr %",
       round(sum(case when bdr_null = 2 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "2 bdr %",
       round(sum(case when bdr_null = 3 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "3 bdr %",
       round(sum(case when bdr_null = 4 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "4 bdr %",
       round(sum(case when bdr_null = 5 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "5 bdr %",
       round(sum(case when bdr_null = 6 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "6 bdr %",
       round(sum(case when bdr_null = 7 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "7 bdr %",
       round(sum(case when bdr_null = 8 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "8 bdr %",
       round(sum(case when bdr_null = 9 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "9 bdr %",
       round(sum(case when bdr_null = 10 then 1 else 0 end) * 100.0 / count(gi.game_id), 2) as "10 bdr %"
from (
         select gi.game_id, count(*) as bdr_null
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
         group by gi.game_id
     ) t
right join game_id_ gi on t.game_id = gi.game_id
join games g on g.game_id = gi.game_id
join players_list pl on pl.player = any(g.players)
group by pl.player
order by pl.player;

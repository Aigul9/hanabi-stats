--
select concat('hanab.live/replay/', g.game_id, '#', turn_action)
from card_actions ca
join games g on ca.game_id = g.game_id
join variants v on g.variant_id = v.variant_id
where num_players = 3
  and 'Valetta6789' = any(players)
  and array_position(players, 'Fireheart') = iif(
      array_position(players, 'Valetta6789') + 1 > num_players,
      1,
      array_position(players, 'Valetta6789') + 1
    )
  and player = 'Fireheart'
  and action_type = 'play'
  and card_rank = 3
  and array_length(suits, 1) in (5, 6)
  and g.variant not like 'Up%'
  and g.variant not like 'Throw%'
  and turn_action - 1 in (
      select turn_clued
      from clues c
      where clue_giver = 'Valetta6789'
      and clue_receiver != 'Fireheart'
      and c.game_id = ca.game_id
    )
order by g.game_id, turn_action;
--   and g.game_id in (
--       select game_id
--       from (
--           select game_id, count(*) as count
--           from card_actions
--           where player = 'Fireheart'
--             and card_rank = 3
--           group by game_id
--           ) as gic
--       where count >= 3
--     )

select (ARRAY[4, 5, 6])[array_position(ARRAY[4, 5, 6], 6) + 1];
select (ARRAY[4, 5, 6])[3];

--search
--1) Fireheart played 3 in 3p game after Val gave clue to a player going after him

--2) Fireheart clued 3 with rank on slot 1 in 4p game to a player in front of me: Fire-Val-Player x
--card next to it is y1
select distinct concat('hanab.live/replay/', g.game_id, '#', turn_action)
from card_actions ca
join games g on ca.game_id = g.game_id
join variants v on g.variant_id = v.variant_id
where 'Valetta6789' = any(players)
  and 'Fireheart' = any(players)
  and array_position(players, 'Fireheart') =
      iif(
          array_position(players, 'Valetta6789') - 1 < 1,
          num_players,
          array_position(players, 'Valetta6789') - 1
        )
  and num_players = 4
  and g.variant not like 'Up%'
  and g.variant not like 'Throw%'
  and array_length(suits, 1) in (5, 6)
  and turn_action - 1 in (
        select turn_clued
        from clues c
        where clue_giver = 'Fireheart'
          and clue_receiver = players[iif(
                array_position(players, 'Valetta6789') + 1 > num_players,
                1,
                array_position(players, 'Valetta6789') + 1
            )]
          and c.game_id = ca.game_id
          and clue = '3'
    );
--hanab.live/replay/98512#14

select 5 > cast(num_players as int) from games limit 1;
select date('2020-04-25 06:36:00.000000') = '2020-04-25';
select ARRAY[1, 2, 3] <@ ARRAY[2, 5, 1, 3];

create function iif(bool, int, int)
RETURNS int AS $$
    BEGIN
        IF $1 = true THEN RETURN $2;
        ELSE RETURN $3;
        END IF;
    END;
$$ LANGUAGE 'plpgsql';

--player's hand on the particular turn
with variables as (
    select 367460 as g_id
)
select turn as turn_moved, slot, card_index, player, card_suit,
       card_rank, turn_drawn, turn_action
from (
         select *,
                rank() over (partition by card_index order by slot desc) as rank_slot
         from (
                  select turn,
                         slot,
                         player,
                         card_suit,
                         card_rank,
                         s.card_index,
                         turn_drawn,
                         turn_action,
                         rank() over (partition by slot, player order by turn desc, player) as rank
                  from slots s
                           join card_actions ca
                                on s.game_id = ca.game_id and s.card_index = ca.card_index
                  where s.game_id = (select g_id from variables)
--     and player = 'kopen'
--     and turn <= 73
                    and turn <= (select max(turn) from slots where game_id = (select g_id from variables))
              ) as dt
         where rank = 1
     ) dt2
where rank_slot = 1
order by player, slot;

--cards played on the last round without drawing any more cards
select card_index,
       turn,
       slot,
       card_suit,
       card_rank,
       player,
       turn_drawn,
       turn_action
from (
         select s.card_index,
                turn,
                slot,
                card_suit,
                card_rank,
                player,
                turn_drawn,
                turn_action,
                rank() over (partition by s.card_index order by slot desc) as rank_slot
         from slots s
                  join card_actions ca
                       on s.game_id = ca.game_id and s.card_index = ca.card_index
         where s.game_id = 367460
           and turn_action >
               (
                   select max(turn_drawn)
                   from card_actions
                   where game_id = 367460
                     and player = ca.player
                   group by player
               )
     ) as t
where rank_slot = 1
order by turn, card_index;

--final state of hands
with variables as (
    select 367460 as g_id
)
select turn as turn_moved, slot, card_index, player, card_suit,
       card_rank, turn_drawn, turn_action
from (select *,
             rank() over (partition by card_index order by slot desc) as rank_slot
      from (
               select turn,
                      slot,
                      player,
                      card_suit,
                      card_rank,
                      s.card_index,
                      turn_drawn,
                      turn_action,
                      rank() over (partition by slot, player order by turn desc, player) as rank
               from slots s
                        join card_actions ca
                             on s.game_id = ca.game_id and s.card_index = ca.card_index
               where s.game_id = (select g_id from variables)
--     and player = 'kopen'
--     and turn <= 73
                 and turn <= (select max(turn)
                              from slots
                              where game_id = (select g_id from variables))
           ) as dt
      where rank = 1
     ) dt2
where rank_slot = 1
and card_index not in (
    select card_index
    from (
             select s.card_index                                               as card_index,
                    rank() over (partition by s.card_index order by slot desc) as rank_slot
             from slots s
                      join card_actions ca
                           on s.game_id = ca.game_id and s.card_index = ca.card_index
             where s.game_id = 367460
               and turn_action >
                   (
                       select max(turn_drawn)
                       from card_actions
                       where game_id = 367460
                         and player = ca.player
                       group by player
                   )
         ) as t
    where rank_slot = 1
)
order by player, slot;

--Games where b1 were played from slot 2
select concat('hanab.live/replay/', t.game_id, '#', turn_action), player from
(select max(slot) as slot_played, s.game_id, s.card_index, card_suit, card_rank
from slots s join card_actions ca on s.game_id = ca.game_id and s.card_index = ca.card_index
join games g on ca.game_id = g.game_id
where players <@ ARRAY['timotree', 'Jillb363636']
and card_suit = 'Blue'
and card_rank = 1
and action_type = 'play'
-- and player = 'Jillb363636'
and turn != 0
group by s.game_id, s.card_index, card_suit, card_rank
having max(slot) = 2) t join card_actions ca
on t.game_id = ca.game_id and t.card_index = ca.card_index
order by t.game_id desc;

--Slot from which the card was played
select max(slot) as slot_played, s.game_id, s.card_index, card_suit, card_rank
from slots s join card_actions ca on s.game_id = ca.game_id and s.card_index = ca.card_index
where s.game_id = 475075
group by s.game_id, s.card_index, card_suit, card_rank
order by card_index;

--my missing scores (not working yet)
select * from variants v
left join games g
on v.variant_id = g.variant_id
where ('Valetta6789' = any(players) or players is null)
group by v.variant, v.variant_id, max_score
having (max(score) != max_score or max(score) is null)
order by 2;

select g.variant_id, g.variant, max(score) from games g
left join variants v on g.variant_id = v.variant_id
where 'Valetta6789' = any(players)
and g.variant_id = 1725
group by g.variant_id, g.variant;

select * from variants;

select distinct variant from games where 'Valetta6789' = any(players);

--group time by months
with dates as (
    select unnest(players)                                            as p,
           date_time_started                                          as s,
           date_time_finished                                         as f,
           date_time_finished - date_time_started                     as d,
           extract(epoch from date_time_finished - date_time_started) as total_diff,
           extract(year from date_time_started)                       as ys,
           extract(year from date_time_finished)                      as yf,
           extract(month from date_time_started)                      as ms,
           extract(month from date_time_finished)                     as mf
    from games
--     where speedrun is false
)
select p as player, ys as year, ms as month, (sum(time_in_sec) / 3600)::int as time
from (select p,
             ys,
             ms,
             case
                 when ms != mf then
                     extract(epoch from date_trunc('month', f) - s)
                 else total_diff
                 end as time_in_sec
      from dates
      union all
      select p,
             yf,
             mf,
             case
                 when ms != mf then
                     extract(epoch from f - date_trunc('month', f))
                 else 0
                 end
      from dates
     ) un
where p in (
            'Valetta6789',
            'RaKXeR',
            'Libster',
            'NoMercy',
            'florrat2',
            'timotree')
group by player, year, month
order by 1, 2, 3;

--check
select extract(epoch from sum(date_time_finished - date_time_started)) from games
where 'Valetta6789' = any(players)
and extract(year from date_time_started) = 2020
and extract(month from date_time_started) = 5;

select * from games where extract(year from date_time_started) = 2020
and extract(month from date_time_started)  = 5;

--last day and hour of the month
select (date_trunc('month', timestamp '2019-09-16 10:33:09.000000') + interval '1 month' - interval '1 second');

--test
select * from games where extract(year from date_time_started) != extract(year from date_time_finished);
select * from games where extract(month from date_time_started) != extract(month from date_time_finished);
select * from games where extract(day from date_time_started) != extract(day from date_time_finished);
select * from games where extract(hour from date_time_started) != extract(hour from date_time_finished);

--copy
-- select *
-- from (select date_time_started,
--              date_time_finished,
--              extract(year from date_time_started)    as ys,
--              extract(year from date_time_finished)   as yf,
--              extract(month from date_time_started)   as ms,
--              extract(month from date_time_finished)  as mf,
--              extract(day from date_time_started)     as ds,
--              extract(day from date_time_finished)    as df,
--              extract(hour from date_time_started)    as hs,
--              extract(hour from date_time_finished)   as hf,
--              extract(minute from date_time_started)  as ms,
--              extract(minute from date_time_finished) as mf,
--              extract(second from date_time_started)  as ss,
--              extract(second from date_time_finished) as sf
--       from games
--       where game_id = 63598
--      ) dates;
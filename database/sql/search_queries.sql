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
select player, year,
       TO_CHAR(
           TO_DATE (month::text, 'MM')
           , 'Month') as month,
       hours, rank
from (
         select player, year, month, hours, rank() over (partition by year, month order by hours desc) as rank
         from (select p as player, ys as year, ms as month, (sum(time_in_sec) / 3600)::int as hours
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
-- where p
-- in
--       (
--        'Valetta6789',
--        'kimbifille',
--        'Lanvin'
-- --        'RaKXeR',
-- --        'Libster',
-- --        'NoMercy',
-- --        'florrat2',
-- --        'timotree'
--           )
               group by player, year, month
              ) t
     ) t_rank
where player = 'scharkbite';
-- where rank = 1;
-- order by year, month, hours desc;

SELECT TO_CHAR(
    TO_DATE (12::text, 'MM'), 'Month'
    ) AS "Month Name";

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

--competition 21.09.2021
select * from games where variant = 'Black (5 Suits)' and detrimental_characters is true
and date(date_time_started) >= '2021-09-03';

--each player's peak
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
)
select player, year, TO_CHAR(
    TO_DATE (month::text, 'MM'), 'Month'
    ) as month, hours
from (
         select player, year, month, hours, rank() over (partition by player order by hours desc) as rank
         from (select p as player, ys as year, ms as month, (sum(time_in_sec) / 3600)::int as hours
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
               where p in (select * from players_list)
               group by player, year, month
              ) t
     ) t_rank
where rank = 1;
-- order by year, month, hours desc;

--Valetta's games
select to_char(date_time_started at time zone 'UTC+3', 'DD.MM.YYYY HH24:MI') as started,
       concat(extract(minutes from date_time_finished-date_time_started), ' min') as duration,
       speedrun,
       variant,
       num_players,
       score,
       players,
       concat('hanab.live/replay/', game_id) as link
from games
where 'Valetta6789' = any(players)
order by game_id;

select distinct concat('hanab.live/replay/', s.game_id, '#', turn) from slots s
join card_actions ca on s.game_id = ca.game_id
join games g on ca.game_id = g.game_id
where slot = 5 and 'Valetta6789' = any(players) and s.game_id <= 52942 and card_rank = 1
and player = 'Valetta6789'
and turn > 10;

select distinct
                concat('hanab.live/replay/', s.game_id, '#', turn_clued)
from clues c join slots s on c.game_id = s.game_id
where s.game_id <= 52942 and clue_receiver = 'Valetta6789' and clue = '2' and turn_clued > 10;

select min(game_id) from player_notes;

--
select game_id,
       players,
       date_time_started,
       date_time_finished,
       round(extract(epoch from lead(date_time_started) over (order by game_id) - date_time_finished) / 60) as min from games
where 'Valetta6789' = any(players);
-- and num_players != 2 and speedrun is false;

--review_time
select * from reviews order by 1;
select count(*) from reviews;

--convert to time
update reviews set review_time = TO_TIMESTAMP(review_time_orig, 'HH24:MI:SS')::time
where review_time_orig not like '%day%';
--less than 2h
update reviews set review_time = null where extract(hours from review_time) > 1;
--no speedruns
update reviews set review_time = null
where (select speedrun from games where games.game_id = reviews.game_id) is true;
--no 2p
update reviews set review_time = null
where (select num_players from games where games.game_id = reviews.game_id) = 2;
--76947
--terminated games
update reviews set review_time = null
where game_id in (
          select game_id
          from game_actions
          group by game_id
          having count(*) = 1
      );

--long reviews
select * from reviews where extract(hours from review_time) = 1;
--short reviews
select r.game_id, review_time, players, end_condition from reviews r join games g on r.game_id = g.game_id
where extract(minutes from review_time) < 1
  and 'Valetta6789' = any(players);

select * from reviews where review_time is null order by 1;

select * from games
where (
        'Valetta6789' = any (players)
        or 'postmans' = any (players)
        or 'Dr_Kakashi' = any (players)
        or 'Floriman' = any (players)
        or 'scharkbite' = any (players)
    )
and game_id >= 276712
order by 1;

select * from card_actions where game_id = 276712;
select * from game_actions where game_id = 276712;

--Val's review time
select extract(year from date_time_started) as ys,
       extract(month from date_time_started) as ms,
       count(r.review_time),
       (extract(epoch from sum(review_time)) / count(r.review_time) / 60)::int as minutes
from reviews r join games g on r.game_id = g.game_id
where 'Valetta6789' = any(players)
group by 1, 2
order by 1, 2, 3;

--review times for all players
select
--        player,
       count(r.review_time) as games,
       (extract(epoch from sum(review_time)) / count(r.review_time) / 60)::int as minutes
from reviews r join games g on r.game_id = g.game_id
-- join players_list pl on pl.player = any(players)
where 'sankala' = any(players)
group by 1
order by 2 desc, 1;

select count(*) from games
where 'ADrone' = any(players)
  and num_players != 2
and speedrun is false;

select count(*) from games
where players @> ARRAY['ADrone'::varchar, 'RaKXeR'];

select * from games
where 'Valetta6789' = any(players)
and 'ADrone' = any(players)
and speedrun is false
order by date_time_started;

--Number of teammates
select player, count(distinct p) as teammates
from (select player, unnest(players) p from games g join players_list pl
    on pl.player = any(players)) t
group by player
order by 2 desc, 1;

-- --draft
-- --groups of players who never played with each other
-- with gen_players as (
--     select ARRAY [pl1.player, pl2.player, pl3.player] as players_row
--     from players_list pl1
--              join players_list pl2
--                   on pl1.player != pl2.player
--     join players_list pl3
--                   on pl2.player != pl3.player
--     and pl1.player != pl3.player
-- )
-- select players_row from gen_players where players_row not in
-- (select distinct players from games);
--
-- select ARRAY['ADrone','asaelr','Dr_Kakashi'] < ARRAY['ADrone','asaelr','Dr_Kakashi', 'Val'];
--
-- --a <@ b b contains a
--
--2p
with gen_players as (
    select pl1.player as pl1, pl2.player as pl2
    from players_list pl1
             join players_list pl2
                  on pl1.player != pl2.player
)
select distinct pl1, pl2, count(*) from gen_players gp
where (
              select count(*)
              from games
              where pl1 = any (players)
                and pl2 = any (players)
          ) < 1
group by pl1, pl2;
--918 existing pairs
--138 non-existing pairs

-- --3p
-- with gen_players as (
--     select pl1.player as pl1, pl2.player as pl2, pl3.player as pl3
--     from players_list pl1
--              join players_list pl2
--                   on pl1.player != pl2.player
--              join players_list pl3
--                   on pl2.player != pl3.player
--                       and pl1.player != pl3.player
-- )
-- select pl1, pl2, pl3 from gen_players where
-- (select count(*)
-- from (select *
-- from (select game_id from games where pl1 = any(players)) as t1
-- join (select game_id from games where pl2 = any(players)) as t2 on t1.game_id = t2.game_id
-- join (select game_id from games where pl3 = any(players)) as t3 on t2.game_id = t3.game_id) t) != 0
-- order by 1, 2;

--slowest games
select player,
       date_time_finished - date_time_started as diff,
       game_id,
       variant,
       players,
       date_time_started,
       date_time_finished,
       seed
from (select *,
             rank() over (partition by player order by date_time_finished - date_time_started desc) as rank
      from players_list pl
               join games g
                    on player = any (players)
      where player in (select * from players_list)
     ) t
where rank = 1
order by 2 desc;

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
--106756 games

--plays, misplays, discards, clues ratio
select player,
--        round(plays * 1.0 / total_pmd, 2) as plays_r,
--        round(misplays * 1.0 / total_pmd, 2) as misplays_r,
--        round(discards * 1.0 / total_pmd, 2) as discards_r,
       round(clues * 1.0 / total_clues, 2) as clues_r,
--        plays,
--        misplays,
--        discards,
       clues,
--        total_pmd as games_pmd
       total_clues as games_clues
from (select player,
       count(*) filter (where action_type = 'play') as plays,
       count(*) filter (where action_type = 'misplay') as misplays,
       count(*) filter (where action_type = 'discard') as discards,
       count(distinct ca.game_id) total_pmd
from card_actions ca
join games g on ca.game_id = g.game_id
where player in (select * from players_list)
and speedrun is false
and num_players != 2
group by player) t1
join
(select clue_giver, count(*) as clues, count(distinct c.game_id) as total_clues from clues c
join games g on c.game_id = g.game_id
where clue_giver in (select * from players_list)
and speedrun is false
and num_players != 2
group by clue_giver) t2
on t1.player = t2.clue_giver
order by 2 desc, 1;

--player who stroke out the game
select t1.player,
       round("third strikes" * 1.0 / count, 2),
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

--winning streak
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

--group by num_players
select *, "2p_ratio" + "3p_ratio" + "4p_ratio" + "5p_ratio" + "6p_ratio" as check
from (select player,
             round(p2 * 1.0 / total, 2) as "2p_ratio",
             round(p3 * 1.0 / total, 2) as "3p_ratio",
             round(p4 * 1.0 / total, 2) as "4p_ratio",
             round(p5 * 1.0 / total, 2) as "5p_ratio",
             round(p6 * 1.0 / total, 2) as "6p_ratio",
             p2                         as "2p_count",
             p3                         as "3p_count",
             p4                         as "4p_count",
             p5                         as "5p_count",
             p6                         as "6p_count",
             total
      from (select player,
                   count(*) filter ( where num_players = 2 ) as p2,
                   count(*) filter ( where num_players = 3 ) as p3,
                   count(*) filter ( where num_players = 4 ) as p4,
                   count(*) filter ( where num_players = 5 ) as p5,
                   count(*) filter ( where num_players = 6 ) as p6,
                   count(*)                                  as total
            from players_list pl
                     join games g
                          on pl.player = any (players)
            where speedrun is false
            group by player
           ) t1
     ) t2
order by 1;

--My games with 0 clues
select * from games g
left join clues c on g.game_id = c.game_id
where c.game_id is null
and 'Valetta6789' = any(players)
and speedrun is false
and detrimental_characters is false
and end_condition = 1;

select count(*) from games
where 'Valetta6789' = any(players)
and speedrun is false
and detrimental_characters is false
and end_condition = 1;
--2433

select count(distinct c.game_id) from clues c
join games g on c.game_id = g.game_id
where 'Valetta6789' != clue_giver
and 'Valetta6789' = any(players)
and speedrun is false
and detrimental_characters is false
and end_condition = 1;
--2433

--Val's max clue starved
select * from games g
join variants v
on g.variant_id = v.variant_id
where g.variant like '%Starved%'
and 'Valetta6789' = any(players)
and score = max_score
and num_players != 2
and speedrun is false
and detrimental_characters is false;

--fav variants by players
with players as (
    select distinct unnest(players) player from games
)
select *
from (
         select *, rank() over (partition by player order by count desc) as rank
         from (
                  select player, variant, count(*) as count
                  from (select *
                        from players
                        where player in (select * from players_list)) t
                           join games g
                                on player = any (g.players)
                                    and speedrun is false
                  group by player, variant) t1
     )t2
where rank = 1
order by 1;
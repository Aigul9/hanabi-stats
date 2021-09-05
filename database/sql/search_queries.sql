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
select turn, slot, player, card_suit,
       card_rank, card_index, turn_drawn, turn_action
from (
    select turn as turn, slot, player, card_suit,
       card_rank, s.card_index, turn_drawn, turn_action,
           rank() over (partition by slot, player order by turn desc, player) as rank
    from slots s join card_actions ca
           on s.game_id = ca.game_id and s.card_index = ca.card_index
    where player = 'Zamiel'
    and turn <= 18
) as dt
where rank = 1;
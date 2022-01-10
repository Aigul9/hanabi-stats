select g.game_id, max(turn_action)from games g
join card_actions ca on g.game_id = ca.game_id
where num_players = 3
  and end_condition = 1
  and variant = 'No Variant'
  and g.game_id not in (select * from bugged_games)
  and speedrun is false
  and all_or_nothing is false
  and one_extra_card is false
  and one_less_card is false
group by g.game_id;

select * from card_actions where game_id = 4761;
select * from game_actions where game_id = 4761;

select * from bugged_games;

--seeds
select distinct seed, max(turn_action)from games g
join card_actions ca on g.game_id = ca.game_id
where num_players = 3
  and end_condition = 1
  and variant = 'No Variant'
  and g.game_id not in (select * from bugged_games)
  and speedrun is false
  and all_or_nothing is false
  and one_extra_card is false
  and one_less_card is false
group by seed;

--stephen
select total, term, round(term * 100.0 / total) as perc
from (select count(*) as total,
    count(*) filter (where end_condition = 4) as term from games
    where num_players = 2
    and 'Dr_Kakashi' = any (players)
    and 'kimbifille' = any (players)
    and speedrun is false
    ) t;
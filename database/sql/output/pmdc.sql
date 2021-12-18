--clues
select clue_giver as player,
       round(clues * 1.0 / total_clues, 2) as clues_r,
       clues,
       total_clues as games_clues
from
(select clue_giver, count(*) as clues, count(distinct c.game_id) as total_clues from clues c
join games g on c.game_id = g.game_id
where clue_giver in (select * from players_list)
and speedrun is false
and num_players != 2
group by clue_giver) t2
order by 2 desc, 1;

--plays
select player,
       round(plays * 1.0 / total_pmd, 2) as plays_r,
       plays,
       total_pmd as games_pmd
from (select player,
       count(*) filter (where action_type = 'play') as plays,
       count(distinct ca.game_id) total_pmd
from card_actions ca
join games g on ca.game_id = g.game_id
where player in (select * from players_list)
and speedrun is false
and num_players != 2
group by player) t1
order by 2 desc, 1;

--misplays
select player,
       round(misplays * 1.0 / total_pmd, 2) as misplays_r,
       misplays,
       total_pmd as games_pmd
from (select player,
       count(*) filter (where action_type = 'misplay') as misplays,
       count(distinct ca.game_id) total_pmd
from card_actions ca
join games g on ca.game_id = g.game_id
where player in (select * from players_list)
and speedrun is false
and num_players != 2
group by player) t1
order by 2 desc, 1;

--discards
select player,
       round(discards * 1.0 / total_pmd, 2) as discards_r,
       discards,
       total_pmd as games_pmd
from (select player,
       count(*) filter (where action_type = 'discard') as discards,
       count(distinct ca.game_id) total_pmd
from card_actions ca
join games g on ca.game_id = g.game_id
where player in (select * from players_list)
and speedrun is false
and num_players != 2
group by player) t1
order by 2 desc, 1;
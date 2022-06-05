--clues
select clue_giver as player,
       round(clues * 1.0 / total_clues, 2) as ratio,
       clues,
       total_clues as games
from
(select clue_giver, count(*) as clues, count(distinct c.game_id) as total_clues from clues c
join games g on c.game_id = g.game_id
where clue_giver in (select * from players_list)
and speedrun is false
and num_players != 2
and variant != 'No Variant'
group by clue_giver) t2
order by 2 desc, 1;
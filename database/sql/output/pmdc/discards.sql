--discards
select player,
       round(discards * 1.0 / total_pmd, 2) as ratio,
       discards,
       total_pmd as games
from (select player,
       count(*) filter (where action_type = 'discard') as discards,
       count(distinct ca.game_id) total_pmd
from card_actions ca
join games g on ca.game_id = g.game_id
where player in (select * from players_list)
and speedrun is false
and num_players != 2
and variant != 'No Variant'
group by player) t1
order by 2 desc, 1;
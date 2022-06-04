select player,
       sum(case when suits = 6 then count else 0 end) as "6 Suits",
       sum(case when suits = 5 then count else 0 end) as "5 Suits",
       sum(case when suits = 4 then count else 0 end) as "4 Suits",
       sum(case when suits = 3 then count else 0 end) as "3 Suits"
from
(select player, max_score / 5 as suits, count(*) as count from players_list p join games g
on player = any(players)
join variants v on g.variant_id = v.variant_id
where num_players != 2
and speedrun is false
and g.variant != 'No Variant'
group by player, max_score / 5) t
group by player;

select * from players_list
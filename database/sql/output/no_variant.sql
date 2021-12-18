--top no vars
with players as (
    select distinct unnest(players) player from games
)
select player, count(*) from players p join games g
on p.player = any(players)
where player in (select * from players_list)
and variant like '%No Variant%'
and speedrun is false
and num_players != 2
group by player
order by 2 desc;
--wins / games for players in players list, excluding speedruns
select players, round(wins * 100.0 / games, 2) as wr, wins, games
from (
         select array_to_string(players, ', ') as players, sum(wins) as wins, sum(games) as games
         from (
                  select array_sort(players)                       as players,
                         count(*) filter (where score = max_score) as wins,
                         count(*)                                  as games
                  from games g
                           join variants v on g.variant = v.variant
                  where speedrun is false
                    and players && (select array_agg(player) from players_list)
                  group by players
              ) t
         where games > 50
         group by array_to_string(players, ', ')
     ) t1
order by 2 desc, 1;

CREATE OR REPLACE FUNCTION array_sort (ANYARRAY)
RETURNS ANYARRAY LANGUAGE SQL
AS $$
SELECT ARRAY(SELECT unnest($1) ORDER BY 1)
$$;
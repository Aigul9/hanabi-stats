use [hanabi_stats]

select * from players
select * from stat

alter table stat
add MaxScore int

alter table stat
add Suits int

update stat set MaxScore = Suits * 5

update stat set Suits = 
case 
when Variant = '3 Suits' then 3
when Variant = '4 Suits' then 4
when Variant = 'No Variant' then 5
when Variant in ('6 Suits', 'Dual-Color Mix', 'Ambiguous Mix', 'Ambiguous & Dual-Color') then 6
else convert(int, substring(reverse(Variant), 8, 1))
end

select * from variants where isNumeric(substring(Variant, charindex('(', Variant) + 1, 1))=0

select * from stat where MaxScore is NULL

select * from stat s, players p
where s.Players like '%' + p.Player + '%'
order by ID

--average score
select p.Player, avg(convert(int, score)) from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] = 2
group by p.Player
order by 2 desc

select p.Player, avg(convert(int, score)) from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] > 2
group by p.Player
order by 2 desc

--number of winnings
select p.Player, count(*), Total2p from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] = 2
and Score=MaxScore
group by p.Player, Total2p
order by 2 desc

select p.Player, count(*), Total3p from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] > 2
and Score=MaxScore
and Total3p >= 100
group by p.Player, Total3p
order by 2 desc

--percentage of winnings
alter table players
add Total2p int

alter table players
add Total2pHard int

alter table players
add Total2pEasy int

alter table players
add Total3pHard int

alter table players
add Total3pEasy int

alter table players
add Total3p int

select * from players

update players set Total2p = 
(select count(*) from stat where players like '%' + player + '%'
and [# of Players] = 2)

update players set Total3p = 
(select count(*) from stat where players like '%' + player + '%'
and [# of Players] > 2)

select player, cast(CAST(c AS float) / CAST(Total2p AS float) * 100 as decimal(10, 2)) as '%', Total2p from
(select player, Total2p, count(*) as c from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] = 2
and Score=MaxScore
group by p.Player, Total2p) t
order by Total2p desc

select * from players
select * from stat

--easy
select player, cast(CAST(c AS float) / CAST(Total2pEasy AS float) * 100 as decimal(10, 2)) as '%',
c as 'Wins2pEasy', Total2pEasy from
(select player, Total2pEasy, count(*) as c from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] = 2
and Score=MaxScore
and EH = 'easy'
group by p.Player, Total2pEasy) t
order by Total2pEasy desc

--hard
select player, cast(CAST(c AS float) / CAST(Total2pHard AS float) * 100 as decimal(10, 2)) as '%',
c as 'Wins2pHard', Total2pHard from
(select player, Total2pHard, count(*) as c from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] = 2
and Score >= MaxScore - 4
and EH = 'hard'
group by p.Player, Total2pHard) t
order by Total2pHard desc

select * from stat
where players like '%Fireheart%'
and [# of Players] = 2
and Score >= MaxScore - 4
and EH = 'hard'

--drop table perc2
select player, c as Wins, Total3p as 'Total3p+',
cast(CAST(c AS float) / CAST(Total3p AS float) * 100 as decimal(10, 2)) as Percentage
into perc2
from
(select player, Total3p, count(*) as c from stat s, players p
where s.Players like '%' + p.Player + '%'
and [# of Players] > 2
and Score=MaxScore
--and Total3p >= 50
group by p.Player, Total3p) t
order by 4 desc, 1

alter table players
add Percentage float

select * from perc2
select * from players

update players set players.Percentage = p2.Percentage
from players p1
inner join perc2 p2
on p1.Player = p2.Player

--select * from players p1
--inner join perc2 p2
--on p1.Player = p2.Player

--groups of players
--self join
select a.player, b.player from players a, players b
where a.Player != b.Player

drop table groupBy2Total
drop table groupBy2Wins

select a.player as ap, b.player as bp, count(*) as Total 
into groupBy2Total
from players a, players b, stat s
where a.Player != b.Player
and a.Player < b.Player
and s.Players like '%' + a.Player + '%'
and s.Players like '%' + b.Player + '%'
and [# of Players] > 2
group by a.Player, b.Player

select a.player as ap, b.player as bp, count(*) as Wins
into groupBy2Wins
from players a, players b, stat s
where a.Player != b.Player
and a.Player < b.Player
and s.Players like '%' + a.Player + '%'
and s.Players like '%' + b.Player + '%'
and [# of Players] > 2
and Score = MaxScore
group by a.Player, b.Player

drop table groupBy2

select g1.ap, g1.bp, Wins, Total, cast(CAST(Wins AS float) / CAST(Total AS float) * 100 as decimal(10, 2)) as '%'
into groupBy2
from groupBy2Total g1, groupBy2Wins g2
where g1.ap = g2.ap
and g1.bp = g2.bp

select * from groupBy2 order by Total desc

--MAIN
select * from players
select * from perc2

select ap as 'Player A', bp as 'Player B',
pc1.Wins as 'Wins A', p1.Total3p as 'Total A',
pc2.Wins as 'Wins B', p2.Total3p as 'Total B',
p1.Percentage as 'Winrate A', 
p2.Percentage as 'Winrate B',
g.Wins, Total, g.Percentage as 'Common Winrate',
cast(g.Percentage - p1.Percentage as decimal(10, 2)) as 'Diff A',
cast(g.Percentage - p2.Percentage as decimal(10, 2)) as 'Diff B',
iif(g.Percentage - p1.Percentage > 0 and g.Percentage - p2.Percentage > 0, 'match', '') as 'Match'
from groupBy2 g, players p1, players p2, perc2 pc1, perc2 pc2
where Total >= 50
and p1.Player = ap
and p2.Player = bp
and pc1.Player = ap
and pc2.Player = bp
order by g.Percentage desc



select ap as 'Player A', bp as 'Player B', cp as 'Player C',
pc1.Wins as 'Wins A', p1.Total3p as 'Total A',
pc2.Wins as 'Wins B', p2.Total3p as 'Total B',
pc3.Wins as 'Wins C', p3.Total3p as 'Total C',
p1.Percentage as 'Winrate A', 
p2.Percentage as 'Winrate B',
p3.Percentage as 'Winrate C',
g.Wins, Total, g.Percentage as 'Common Winrate',
cast(g.Percentage - p1.Percentage as decimal(10, 2)) as 'Diff A',
cast(g.Percentage - p2.Percentage as decimal(10, 2)) as 'Diff B',
cast(g.Percentage - p3.Percentage as decimal(10, 2)) as 'Diff C',
iif(g.Percentage - p1.Percentage > 0 and g.Percentage - p2.Percentage > 0
and g.Percentage - p3.Percentage > 0, 'match', '') as 'Match'
from groupBy3 g, players p1, players p2, players p3, perc2 pc1, perc2 pc2, perc2 pc3
where g.Wins >= 10
and p1.Player = ap
and p2.Player = bp
and p3.Player = cp
and pc1.Player = ap
and pc2.Player = bp
and pc3.Player = cp
order by g.Percentage desc



select * from groupBy2 where ap = 'Zamiel' or bp = 'Zamiel'
select * from groupBy2 where ap = 'micerang' or bp = 'micerang' order by Percentage desc

select * from groupBy2Total

--group of 3
select a.player as ap, b.player as bp, c.player as cp, count(*) as Total 
into groupBy3Total
from players a, players b, players c, stat s
where a.Player != b.Player
and a.Player != c.Player
and a.Player < b.Player
and b.Player < c.Player
and s.Players like '%' + a.Player + '%'
and s.Players like '%' + b.Player + '%'
and s.Players like '%' + c.Player + '%'
and [# of Players] > 2
group by a.Player, b.Player, c.Player

select * from groupBy3Total
select count(Total) from groupBy3Total
select count(ID) from stat where [# of Players] = 4

select a.player as ap, b.player as bp, c.player as cp, count(*) as Wins 
into groupBy3Wins
from players a, players b, players c, stat s
where a.Player != b.Player
and a.Player != c.Player
and a.Player < b.Player
and b.Player < c.Player
and s.Players like '%' + a.Player + '%'
and s.Players like '%' + b.Player + '%'
and s.Players like '%' + c.Player + '%'
and [# of Players] > 2
and Score = MaxScore
group by a.Player, b.Player, c.Player

select g1.ap, g1.bp, g1.cp, Wins, Total, cast(CAST(Wins AS float) / CAST(Total AS float) * 100 as decimal(10, 2)) as '%'
into groupBy3
from groupBy3Total g1, groupBy3Wins g2
where g1.ap = g2.ap
and g1.bp = g2.bp
and g1.cp = g2.cp

select * from groupBy3 order by Total desc
select * from groupBy3
--order by 1, 2, 3
where Total >= 20
order by Percentage desc

select * from stat s
where s.Players like '%' + 'asaelr' + '%'
and s.Players like '%' + 'Floriman' + '%'
and Score = MaxScore

--variant types
drop table var_type_full
select Variant, Type, [2-player], [3 4-player], [5-player], [6-player]
into var_type_full
from [dbo].[variant_types] v
left join [dbo].[typesFromDoc] t
on v.Type = t.[Variant Type]

select * from var_type_full

alter table var_type_full
add EH2 varchar(4)
alter table var_type_full
add EH34 varchar(4)
alter table var_type_full
add EH5 varchar(4)
alter table var_type_full
add EH6 varchar(4)

alter table var_type_full
alter column EH2 varchar(255)
alter table var_type_full
alter column EH34 varchar(255)
alter table var_type_full
alter column EH5 varchar(255)
alter table var_type_full
alter column EH6 varchar(255)
alter table stat
alter column EH varchar(255)

update var_type_full set [EH2] = 'middle hard' where ([Type] like '%1x%' or [Type] = 'Null') and [EH2] = 'easy'
update var_type_full set [EH34] = 'middle hard' where ([Type] like '%1x%' or [Type] = 'Null') and [EH34] = 'easy'
update var_type_full set [EH5] = 'middle hard' where ([Type] like '%1x%' or [Type] = 'Null') and [EH5] = 'easy'
update var_type_full set [EH6] = 'middle hard' where ([Type] like '%1x%' or [Type] = 'Null') and [EH6] = 'easy'
update var_type_full set [EH2] = 'hard' where [Type] like '%2x%'

update var_type_full set [EH2] = 'hard' where [Variant] like '%Duck%' or [Variant] like '%Number%Blind%'
update var_type_full set [EH34] = ' hard' where [Variant] like '%Duck%' or [Variant] like '%Number%Blind%'
update var_type_full set [EH5] = 'hard' where [Variant] like '%Duck%' or [Variant] like '%Number%Blind%'
update var_type_full set [EH6] = 'hard' where [Variant] like '%Duck%' or [Variant] like '%Number%Blind%'

update var_type_full set [EH2] = 'middle hard' where [Variant] like '%cow%' and [EH2] = 'easy'
update var_type_full set [EH34] = 'middle hard' where [Variant] like '%cow%' and [EH34] = 'easy'
update var_type_full set [EH5] = 'middle hard' where [Variant] like '%cow%' and [EH5] = 'easy'
update var_type_full set [EH6] = 'middle hard' where [Variant] like '%cow%' and [EH6] = 'easy'

update var_type_full set [EH2] = 'middle hard' where [Variant] like '%throw%' and [EH2] = 'easy'
update var_type_full set [EH34] = 'middle hard' where [Variant] like '%throw%' and [EH34] = 'easy'
update var_type_full set [EH5] = 'middle hard' where [Variant] like '%throw%' and [EH5] = 'easy'
update var_type_full set [EH6] = 'middle hard' where [Variant] like '%throw%' and [EH6] = 'easy'

select * from var_type_full where Variant like '%null %'

update var_type_full
set EH2 = case
	when convert(float, replace([2-player], ',', '.')) >= 1.25 then 'hard'
	else 'easy'
end

update var_type_full
set EH34 = case
	when convert(float, replace([3 4-player], ',', '.')) >= 1.25 then 'hard'
	else 'easy'
end

update var_type_full
set EH5 = case
	when convert(float, replace([5-player], ',', '.')) >= 1.25 then 'hard'
	else 'easy'
end

update var_type_full
set EH6 = case
	when convert(float, replace([6-player], ',', '.')) >= 1.25 then 'hard'
	else 'easy'
end

--number of easy and hard games

--update players set Total2pHard = 
--(select count(*) from stat where players like '%' + player + '%'
--and [# of Players] = 2
--and EH = 'hard')

--update players set Total2pEasy = 
--(select count(*) from stat where players like '%' + player + '%'
--and [# of Players] = 2
--and EH = 'easy')

--update players set Total3pHard = 
--(select count(*) from stat where players like '%' + player + '%'
--and [# of Players] > 2
--and EH = 'hard')

--update players set Total3pEasy = 
--(select count(*) from stat where players like '%' + player + '%'
--and [# of Players] > 2
--and EH = 'easy')

select * from players where Total2p > 50

select * from stat
select distinct EH from stat

alter table stat
add EH nvarchar(4)

update stat set EH = 
case [# of Players]
	when 2 then EH2
	when 3 then EH34
	when 4 then EH34
	when 5 then EH5
	when 6 then EH6
end
from stat s join [dbo].[var_type_full] v
on s.Variant = v.Variant

alter table stat
add Coef int

select * from stat

select * from [dbo].[typesFromDoc]

--coefs
--drop table coefs
--create table coefs (
--	var_type nvarchar(255),
--	coef_win int,
--	coef_lose int,
--)

--insert into coefs values ('1oE', 10, -2)
--insert into coefs values ('Null', 10, -2)
--insert into coefs values ('2oE', 30, 0)
--insert into coefs values ('easy', 1, -10)

select * from var_type_full

--alter table var_type_full
--add coef_win int
--alter table var_type_full
--add coef_lose int

--update var_type_full set coef_win = case
--	when Type = 'Null' then 4
--	when Type like '%1oE%' then 20
--	when Type like '%2oE%' then 50
--	when Variant like 'No Variant' then 0
--	when Variant like '6 Suits' then 0
--	else 2
--end

--update var_type_full set coef_lose = case
--	when Type = 'Null' then 0
--	when Type like '%1oE%' then 0
--	when Type like '%2oE%' then 0
--	when Variant like 'No Variant' then 0
--	when Variant like '6 Suits' then 0
--	when Variant = 'Dark Rainbow (6 Suits)' then 0
--	else -10
--end

update stat set Coef = case
	when Variant = 'No Variant' then 0
	when Variant = '6 Suits' then 0
	when Variant = 'Dark Rainbow (6 Suits)' and WL = 'lose' then 0
	when EH = 'hard' and WL = 'win' then 50
	when EH = 'hard' and WL = 'lose' then 0
	when EH = 'middle hard' and WL = 'win' then 20
	when EH = 'middle hard' and WL = 'lose' then -1
	when EH = 'easy' and WL = 'win' then 2
	when EH = 'easy' and WL = 'lose' then -8
end

alter table stat
add WL nvarchar(4)

select * from stat

update stat set WL = case
	when MaxScore = Score then 'win'
	else 'lose'
end

update stat set WL = 'win'
where EH = 'hard' and Score >= MaxScore - 3

--win/lose coefs
--select player, sum(coef_win) 'win', sum(coef_lose) as 'lose', sum(coef_win) + sum(coef_lose) as 'Diff'
--from players p, stat s, var_type_full v
--where s.Players like '%' + p.Player + '%'
--and s.Variant = v.Variant
--and [# of Players] = 2
--group by player
--order by 4 desc

select Variant, count(*) from stat where players like '%Fireheart%' and WL = 'lose'
and [# of Players] = 2
group by Variant
order by 2 desc

--select a1.player as 'A', a2.player as 'B',
--w1.win as 'CoefWinA', w1.lose as 'CoefLoseA', w2.win as 'CoefWinB', w2.lose as 'CoefLoseB',
---cast(CAST(w1.lose AS float) / CAST(w1.win AS float) * 100 as decimal(10, 2)) as '% A',
---cast(CAST(w2.lose AS float) / CAST(w2.win AS float) * 100 as decimal(10, 2)) as '% B',
---cast(CAST(w1.lose + w2.lose AS float) / CAST(w1.win + w2.win AS float) * 100 as decimal(10, 2)) as 'Common %',
---cast(CAST(w1.lose + w2.lose AS float) / CAST(w1.win + w2.win AS float) * 100 as decimal(10, 2)) +
--cast(CAST(w1.lose AS float) / CAST(w1.win AS float) * 100 as decimal(10, 2)) as 'Diff A %',
---cast(CAST(w1.lose + w2.lose AS float) / CAST(w1.win + w2.win AS float) * 100 as decimal(10, 2)) +
--cast(CAST(w2.lose AS float) / CAST(w2.win AS float) * 100 as decimal(10, 2)) as 'Diff B %'
----iif(g.Percentage - p1.Percentage > 0 and g.Percentage - p2.Percentage > 0, 'match', '') as 'Match'
--into coef_temp
--from players a1, players a2, win_lose_temp w1, win_lose_temp w2, groupBy2 g
--where a1.Player != a2.Player
--and a1.Player < a2.Player
--and a1.Player = w1.Player
--and a2.Player = w2.Player
--and w1.win != 0
--and w2.win != 0
--and a1.Player = ap
--and a2.Player = bp
--and Total >= 50

drop table coef_temp
select * from coef_temp order by 9 desc
select * from groupby2
alter table groupby2
add CoefWins int

select ap, bp, sum(coef_win)
from groupby2 g join stat s
on s.Players like '%' + ap + '%'
and s.Players like '%' + bp + '%'
join var_type_full v on s.Variant = v.Variant
group by ap, bp

select * from stat where players like '%NoAnni%'
and players like '%TimeHoodie%'
select * from var_type_full

select * from stat
select * from var_type_full

select *, iif(abs([Diff A %]) < 10 and abs([Diff B %]) < 10, 'match', '') as 'Match'
from coef_temp

select sum(coef_win) from stat s, var_type_full v
where s.Variant = v.Variant and
players like '%Fireheart%'
and [# of Players] = 2

select * from coef_temp

drop table coef_temp

select player, 0 as 'coef2win', 0 as 'coef2lose', 0 as 'coef3win', 0 as 'coef3lose'  into coef_temp
from players p, stat s
where s.Players like '%' + p.Player + '%'
group by player

update coef_temp set [coef2win] = s from
coef_temp c join
(select player, sum(coef) as s
from players p, stat s
where s.Players like '%' + p.Player + '%'
and s.[# of Players] = 2
and WL = 'win'
group by p.Player) as t
on c.Player = t.Player

update coef_temp set [coef2lose] = s from
coef_temp c join
(select player, sum(coef) as s
from players p, stat s
where s.Players like '%' + p.Player + '%'
and s.[# of Players] = 2
and WL = 'lose'
group by p.Player) as t
on c.Player = t.Player

update coef_temp set [coef3win] = s from
coef_temp c join
(select player, sum(coef) as s
from players p, stat s
where s.Players like '%' + p.Player + '%'
and s.[# of Players] > 2
and WL = 'win'
group by p.Player) as t
on c.Player = t.Player

update coef_temp set [coef3lose] = s from
coef_temp c join
(select player, sum(coef) as s
from players p, stat s
where s.Players like '%' + p.Player + '%'
and s.[# of Players] > 2
and WL = 'lose'
group by p.Player) as t
on c.Player = t.Player

select * from coef_temp

select * from stat where [# of Players] = 2 and Players like '%asaelr%'
select * from stat where [# of Players] = 2 and Players like '%Zamiel%'
select * from stat where [# of Players] = 2 and Variant like '%Dark Rainbow%'

select * from groupby2

update groupby2 set CoefWins = s from
groupBy2 g1 join
(select ap, bp, sum(coef) as s from groupBy2 g, stat s
where s.Players like '%' + ap + '%'
and s.Players like '%' + bp + '%'
and WL = 'win'
group by ap, bp) t
on g1.ap = t.ap
and g1.bp = t.bp

alter table groupby2
add CoefLoses int

update groupby2 set CoefLoses = s from
groupBy2 g1 join
(select ap, bp, sum(coef) as s from groupBy2 g, stat s
where s.Players like '%' + ap + '%'
and s.Players like '%' + bp + '%'
and WL = 'lose'
group by ap, bp) t
on g1.ap = t.ap
and g1.bp = t.bp

select * from stat where [# of Players] > 2 and Players like '%asaelr%' and coef > 0

select * from stat where [# of Players] > 2 and Players like '%Fireheart%' and Players like '%Livia%' and coef > 0
order by coef desc


select * from stat where [# of Players] = 3 and Players like '%Fireheart%' and Players like '%Livia%'
and Variant like '%Pink & Dark Rainbow%'
order by coef desc


select * from var_type_full where Variant like '%Pink & Dark Rainbow%'

select * from coef_temp
select * from groupby2

select * from [dbo].[variant_types]

--loses / wins
drop table main_temp

select a1.player as 'A', a2.player as 'B',
c1.Coef3win as 'Coef win A', c1.Coef3lose as 'Coef lose A',
c2.Coef3win as 'Coef win B', c2.Coef3lose as 'Coef lose B',
CoefWins, CoefLoses,
-cast(CAST(c1.Coef3lose AS float) / CAST(c1.Coef3win AS float) * 100 as decimal(10, 2)) as 'Error % A',
-cast(CAST(c2.Coef3lose AS float) / CAST(c2.Coef3win AS float) * 100 as decimal(10, 2)) as 'Error % B',
-cast(CAST(CoefLoses AS float) / CAST(CoefWins AS float) * 100 as decimal(10, 2)) as 'Common Error %'
into main_temp
from players a1, players a2, coef_temp c1, coef_temp c2, groupby2 g
where a1.Player != a2.Player
and a1.Player < a2.Player
--and a1.Player = w1.Player
--and a2.Player = w2.Player
--and w1.win != 0
--and w2.win != 0
and a1.Player = ap
and a2.Player = bp
and Total >= 50
and c1.player = a1.player
and c2.player = a2.player
and c1.Coef3win != 0
and c2.Coef3win != 0
and CoefWins != 0
and abs(c1.Coef3lose) < abs(c1.Coef3win)
and abs(c2.Coef3lose) < abs(c2.Coef3win)
--27

select *, iif([Common Error %] < [Error % A] and [Common Error %] < [Error % B], 'match', '') as 'Match'
from main_temp
order by [Common Error %] asc
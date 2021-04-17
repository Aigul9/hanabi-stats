use [hanabi_stats]

select * from [dbo].[players] order by 3 desc, 2 desc

select distinct Players, count(*)
from [dbo].[stat] where convert(date, SUBSTRING([Date & Time], 1, 10), 121) < '2020-01-01'
group by Players
order by 2 desc

select * into teachers
from players

alter table teachers
add total float

update teachers set total = 
(select count(*) from stat where players like '%' + player + '%'
and convert(date, SUBSTRING([Date & Time], 1, 10), 121) < '2020-01-01'
)

select player, total from teachers order by 2 desc, 1
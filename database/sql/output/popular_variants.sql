--popular variants
select variant, count(*) from games
group by variant
order by 2 desc;
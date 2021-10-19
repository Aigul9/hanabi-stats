select max(game_id) from games;
--644584 - Neo4j

select * from variants;
select sum(eff_2p) from variants; --1654.3699999999762
select sum(eff_34p) from variants; --1967.8000000000163
select sum(eff_5p) from variants; --2449.7599999999943
select sum(eff_6p) from variants; --2070.3199999999792

ALTER TABLE variants ADD COLUMN eff_2p float;
ALTER TABLE variants ADD COLUMN eff_34p float;
ALTER TABLE variants ADD COLUMN eff_5p float;
ALTER TABLE variants ADD COLUMN eff_6p float;

select * from variants where eff_2p = 1.2; --44 vars
--mark dd 2p vars as hard
update variants set eff_2p = 1.25 where eff_2p = 1.2;

ALTER TABLE games ADD COLUMN eff float;

update games g set eff =
case num_players
when 2 then eff_2p
when 3 then eff_34p
when 4 then eff_34p
when 5 then eff_5p
when 6 then eff_6p
end
from variants v
where g.variant = v.variant;

select * from games;

select count(*) from hyphen_ated;
--153

select * from games
where 'Floriman' = any(players) and 'JerryYang' = any(players)
order by eff;

select * from hyphen_ated order by 1;
delete from hyphen_ated where player = 'wittvector';
delete from hyphen_ated where player = 'Tiramisu2th';
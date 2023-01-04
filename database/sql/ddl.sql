--games
ALTER TABLE games ADD COLUMN starting_player integer;
ALTER TABLE games ADD COLUMN num_players integer;
ALTER TABLE games ADD COLUMN variant_id integer;
ALTER TABLE games ADD COLUMN timed boolean;
ALTER TABLE games ADD COLUMN time_base integer;
ALTER TABLE games ADD COLUMN time_per_turn integer;
ALTER TABLE games ADD COLUMN card_cycle boolean;
ALTER TABLE games ADD COLUMN deck_plays boolean;
ALTER TABLE games ADD COLUMN empty_clues boolean;
ALTER TABLE games ADD COLUMN one_extra_card boolean;
ALTER TABLE games ADD COLUMN one_less_card boolean;
ALTER TABLE games ADD COLUMN all_or_nothing boolean;
ALTER TABLE games ADD COLUMN detrimental_characters boolean;
ALTER TABLE games ADD COLUMN score integer;
ALTER TABLE games ADD COLUMN num_turns integer;
ALTER TABLE games ADD COLUMN end_condition integer;
ALTER TABLE games ADD COLUMN date_time_started timestamp;
ALTER TABLE games ADD COLUMN date_time_finished timestamp;
ALTER TABLE games ADD COLUMN num_games_on_this_seed integer;
ALTER TABLE games ADD COLUMN tags varchar;

ALTER TABLE games ADD CONSTRAINT games_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES variants (variant_id);

--variants
ALTER TABLE variants ADD COLUMN max_score_2p int;
ALTER TABLE variants ADD COLUMN max_score_3p int;
ALTER TABLE variants ADD COLUMN max_score_4p int;
ALTER TABLE variants ADD COLUMN max_score_5p int;
ALTER TABLE variants ADD COLUMN max_score_6p int;

ALTER TABLE variants ADD COLUMN suits varchar[];
ALTER TABLE variants ADD COLUMN special_rank int;
ALTER TABLE variants ADD COLUMN special_deceptive boolean;
ALTER TABLE variants ADD COLUMN special_all_clue_colors boolean;
ALTER TABLE variants ADD COLUMN special_all_clue_ranks boolean;
ALTER TABLE variants ADD COLUMN special_no_clue_colors boolean;
ALTER TABLE variants ADD COLUMN special_no_clue_ranks boolean;
ALTER TABLE variants ADD COLUMN colors varchar[];

--create indices
CREATE INDEX games_index_variant_id ON games (variant_id);
CREATE INDEX games_index_seed ON games (seed);
CREATE INDEX decks_index_seed ON decks (seed);
CREATE INDEX game_actions_index_game_id ON game_actions (game_id);
CREATE INDEX variants_index_variant_id ON variants (variant_id);
CREATE INDEX variants_index_variant ON variants (variant);
CREATE INDEX card_actions_index_game_id ON card_actions (game_id);
CREATE INDEX card_actions_index_card_index ON card_actions (card_index);

create table players_list(
    player varchar(255) primary key
);

drop table bugged_games;
create table bugged_games(
    game_id int primary key,
    test varchar(20)
);

create table reviews(
    game_id int primary key,
    review_time_orig varchar(255)
);

ALTER TABLE reviews ADD COLUMN review_time time;

--h-community
create table hyphen_ated (
    player varchar(255) primary key
);

insert into hyphen_ated
select * from players_list;

insert into hyphen_ated values ('Nitrate2');
insert into hyphen_ated values ('910dan');
insert into hyphen_ated values ('cak199164');
insert into hyphen_ated values ('Cory');
insert into hyphen_ated values ('Ahming');
insert into hyphen_ated values ('Fey');
insert into hyphen_ated values ('Hyphen_ated');
insert into hyphen_ated values ('Instantiation');
insert into hyphen_ated values ('Livia');
insert into hyphen_ated values ('sankala');
insert into hyphen_ated values ('Swifter');
insert into hyphen_ated values ('Kernel');
insert into hyphen_ated values ('ace201');
insert into hyphen_ated values ('aitch2');
insert into hyphen_ated values ('Aluap');
insert into hyphen_ated values ('Amy2');
insert into hyphen_ated values ('Andrew_UK');
insert into hyphen_ated values ('Andrew_DE');
insert into hyphen_ated values ('Animex52');
insert into hyphen_ated values ('anser');
insert into hyphen_ated values ('antitelharsic');
insert into hyphen_ated values ('aquarelle');
insert into hyphen_ated values ('arv');
insert into hyphen_ated values ('avanderwalde');
insert into hyphen_ated values ('awe');
insert into hyphen_ated values ('bjnh');
insert into hyphen_ated values ('BlueNovember');
insert into hyphen_ated values ('boba');
insert into hyphen_ated values ('Bonja');
insert into hyphen_ated values ('CaptainAggro');

insert into hyphen_ated values ('castlesintheair');
insert into hyphen_ated values ('catula');
insert into hyphen_ated values ('ChristopheAF');
insert into hyphen_ated values ('colton');
insert into hyphen_ated values ('corys');
insert into hyphen_ated values ('dancherp');
insert into hyphen_ated values ('DarthGandalf');
insert into hyphen_ated values ('Daryl');
insert into hyphen_ated values ('derekcheah');
insert into hyphen_ated values ('Div');
insert into hyphen_ated values ('dobi');
insert into hyphen_ated values ('duckmammal');
insert into hyphen_ated values ('duckless');
insert into hyphen_ated values ('duckmedic');
insert into hyphen_ated values ('Durandal');
insert into hyphen_ated values ('ejwu');
insert into hyphen_ated values ('elamate');
insert into hyphen_ated values ('eljavi');
insert into hyphen_ated values ('eljobe');
insert into hyphen_ated values ('ellomenop');
insert into hyphen_ated values ('emilyzhao');
insert into hyphen_ated values ('efaust');
insert into hyphen_ated values ('vEnhance');
insert into hyphen_ated values ('Feer');
insert into hyphen_ated values ('fishcat');
insert into hyphen_ated values ('Carunty');
insert into hyphen_ated values ('hakha3');
insert into hyphen_ated values ('HariKrishnan');
insert into hyphen_ated values ('HelanaAshryvr');
insert into hyphen_ated values ('honzas');

insert into hyphen_ated values ('invarse');
insert into hyphen_ated values ('IsabeltheCat');
insert into hyphen_ated values ('jack67889');
insert into hyphen_ated values ('jatloe');
insert into hyphen_ated values ('jaypeg');
insert into hyphen_ated values ('jeep');
insert into hyphen_ated values ('jeff10');
insert into hyphen_ated values ('JerryYang');
insert into hyphen_ated values ('joelwool');
insert into hyphen_ated values ('katian');
insert into hyphen_ated values ('kemurphy');
insert into hyphen_ated values ('kinkajusrevenge');
insert into hyphen_ated values ('kodomazer');
insert into hyphen_ated values ('kooolant');
insert into hyphen_ated values ('kopen');
insert into hyphen_ated values ('ksfortson');
insert into hyphen_ated values ('LaFayette');
insert into hyphen_ated values ('lotem');
insert into hyphen_ated values ('macanek');
insert into hyphen_ated values ('MalachiteMoa');
insert into hyphen_ated values ('MangoPie');
insert into hyphen_ated values ('MarcLovesDogs');
insert into hyphen_ated values ('MasN');
insert into hyphen_ated values ('MathNoob');
insert into hyphen_ated values ('methmatics');
insert into hyphen_ated values ('MKQ');
insert into hyphen_ated values ('newduke');
insert into hyphen_ated values ('newsun');
insert into hyphen_ated values ('NumerateClutter');
insert into hyphen_ated values ('nkarpov');

insert into hyphen_ated values ('Onen');
insert into hyphen_ated values ('orucsoraihc');
insert into hyphen_ated values ('Pimak');
insert into hyphen_ated values ('plus');
insert into hyphen_ated values ('postmans');
insert into hyphen_ated values ('qqqq');
insert into hyphen_ated values ('ReaverSe');
insert into hyphen_ated values ('rkass');
insert into hyphen_ated values ('robense');
insert into hyphen_ated values ('Romain672');
insert into hyphen_ated values ('rs1');
insert into hyphen_ated values ('rz');
insert into hyphen_ated values ('sephiroth');
insert into hyphen_ated values ('squirrel1988');
insert into hyphen_ated values ('Sucubis');
insert into hyphen_ated values ('swineherd');
insert into hyphen_ated values ('Tailz');
insert into hyphen_ated values ('Takis');
insert into hyphen_ated values ('TheDaniMan');
insert into hyphen_ated values ('TimeHoodie');
insert into hyphen_ated values ('Hoodie');
insert into hyphen_ated values ('Tiramisu2th');
insert into hyphen_ated values ('tulioz');
insert into hyphen_ated values ('wjomlex');
insert into hyphen_ated values ('wittvector');
insert into hyphen_ated values ('willwin4sure');
insert into hyphen_ated values ('wortel');
insert into hyphen_ated values ('wump');
insert into hyphen_ated values ('XMIL');
insert into hyphen_ated values ('Zakisan');

insert into hyphen_ated values ('Wittvector');
insert into hyphen_ated values ('will.i.am');
insert into hyphen_ated values ('hanabornoob');
insert into hyphen_ated values ('elamate90');
insert into hyphen_ated values ('Kaznad');
insert into hyphen_ated values ('nishanoire');
insert into hyphen_ated values ('JDepp');
insert into hyphen_ated values ('Matze22');
insert into hyphen_ated values ('caña');
insert into hyphen_ated values ('Plum');
insert into hyphen_ated values ('level_17');
insert into hyphen_ated values ('Veexliat');
insert into hyphen_ated values ('NoAnni');
insert into hyphen_ated values ('SashaIr');
insert into hyphen_ated values ('just_a_dick');
insert into hyphen_ated values ('nmego');
insert into hyphen_ated values ('smallman');
insert into hyphen_ated values ('torp');
insert into hyphen_ated values ('Razvogor');
insert into hyphen_ated values ('Asddsa76');
insert into hyphen_ated values ('skyblueexo');
insert into hyphen_ated values ('fuckthiswebsite');
insert into hyphen_ated values ('eevee');
insert into hyphen_ated values ('fpvandoorn');
insert into hyphen_ated values ('charmander');
insert into hyphen_ated values ('Etherealz');
insert into hyphen_ated values ('dramos');
insert into hyphen_ated values ('BlameItOnRaz');
insert into hyphen_ated values ('Razgovor');
insert into hyphen_ated values ('BlameItOnRaz:D');

insert into hyphen_ated values ('sankala fan');
insert into hyphen_ated values ('IAMJEFFFAN');
insert into hyphen_ated values ('NotRaKXeR');
insert into hyphen_ated values ('xor');
insert into hyphen_ated values ('Chronometrics');
insert into hyphen_ated values ('Ptheven');
insert into hyphen_ated values ('Floribster');
insert into hyphen_ated values ('Floranek');
insert into hyphen_ated values ('Gazrovor');
insert into hyphen_ated values ('Shos');
insert into hyphen_ated values ('Elatekur');
insert into hyphen_ated values ('Lobsterosity');
insert into hyphen_ated values ('magikarp');
insert into hyphen_ated values ('scepheo');
insert into hyphen_ated values ('pipiki');
insert into hyphen_ated values ('pikipi');
insert into hyphen_ated values ('kipipi');
insert into hyphen_ated values ('cequoy');
insert into hyphen_ated values ('DaBeast');
insert into hyphen_ated values ('Fafrd');
insert into hyphen_ated values ('IAMGUESSING');
insert into hyphen_ated values ('mudkip');
insert into hyphen_ated values ('sckuzzle');
insert into hyphen_ated values ('sheamol');
insert into hyphen_ated values ('superbipbip');
insert into hyphen_ated values ('yaiir');
insert into hyphen_ated values ('yuto');
insert into hyphen_ated values ('indegoo');
insert into hyphen_ated values ('indego2');
insert into hyphen_ated values ('Lel0uch2');
insert into hyphen_ated values ('Doge');

--new vars 03.11.2021
insert into variants values (1353, 'Synesthesia (6 Suits)');
insert into variants values (1383, 'Synesthesia (5 Suits)');
insert into variants values (1386, 'Synesthesia (4 Suits)');
insert into variants values (1387, 'Synesthesia (3 Suits)');
insert into variants values (1642, 'Synesthesia & Black (6 Suits)');
insert into variants values (1644, 'Synesthesia & Black (5 Suits)');
insert into variants values (1645, 'Synesthesia & Black (4 Suits)');
insert into variants values (1646, 'Synesthesia & Black (3 Suits)');
insert into variants values (1647, 'Synesthesia & Rainbow (6 Suits)');
insert into variants values (1648, 'Synesthesia & Rainbow (5 Suits)');
insert into variants values (1791, 'Synesthesia & Rainbow (4 Suits)');
insert into variants values (1792, 'Synesthesia & Rainbow (3 Suits)');
insert into variants values (1793, 'Synesthesia & White (6 Suits)');
insert into variants values (1794, 'Synesthesia & White (5 Suits)');
insert into variants values (1795, 'Synesthesia & White (4 Suits)');
insert into variants values (1796, 'Synesthesia & White (3 Suits)');
insert into variants values (1797, 'Synesthesia & Brown (6 Suits)');
insert into variants values (1798, 'Synesthesia & Brown (5 Suits)');
insert into variants values (1799, 'Synesthesia & Brown (4 Suits)');
insert into variants values (1800, 'Synesthesia & Brown (3 Suits)');
insert into variants values (1801, 'Synesthesia & Null (6 Suits)');
insert into variants values (1802, 'Synesthesia & Null (5 Suits)');
insert into variants values (1803, 'Synesthesia & Null (4 Suits)');
insert into variants values (1804, 'Synesthesia & Null (3 Suits)');
insert into variants values (1805, 'Synesthesia & Dark Rainbow (6 Suits)');
insert into variants values (1806, 'Synesthesia & Dark Rainbow (5 Suits)');
insert into variants values (1807, 'Synesthesia & Dark Rainbow (4 Suits)');
insert into variants values (1808, 'Synesthesia & Dark Rainbow (3 Suits)');
insert into variants values (1809, 'Synesthesia & Gray (6 Suits)');
insert into variants values (1810, 'Synesthesia & Gray (5 Suits)');
insert into variants values (1811, 'Synesthesia & Gray (4 Suits)');
insert into variants values (1812, 'Synesthesia & Gray (3 Suits)');
insert into variants values (1813, 'Synesthesia & Dark Brown (6 Suits)');
insert into variants values (1814, 'Synesthesia & Dark Brown (5 Suits)');
insert into variants values (1815, 'Synesthesia & Dark Brown (4 Suits)');
insert into variants values (1816, 'Synesthesia & Dark Brown (3 Suits)');
insert into variants values (1817, 'Synesthesia & Dark Null (6 Suits)');
insert into variants values (1818, 'Synesthesia & Dark Null (5 Suits)');
insert into variants values (1819, 'Synesthesia & Dark Null (4 Suits)');
insert into variants values (1820, 'Synesthesia & Dark Null (3 Suits)');
insert into variants values (1821, 'Critical Fours (6 Suits)');
insert into variants values (1822, 'Critical Fours (5 Suits)');
insert into variants values (1823, 'Critical Fours & Rainbow (6 Suits)');
insert into variants values (1824, 'Critical Fours & Rainbow (5 Suits)');
insert into variants values (1825, 'Critical Fours & Pink (6 Suits)');
insert into variants values (1826, 'Critical Fours & Pink (5 Suits)');
insert into variants values (1827, 'Critical Fours & White (6 Suits)');
insert into variants values (1828, 'Critical Fours & White (5 Suits)');
insert into variants values (1829, 'Critical Fours & Brown (6 Suits)');
insert into variants values (1830, 'Critical Fours & Brown (5 Suits)');
insert into variants values (1831, 'Critical Fours & Omni (6 Suits)');
insert into variants values (1832, 'Critical Fours & Omni (5 Suits)');
insert into variants values (1833, 'Critical Fours & Null (6 Suits)');
insert into variants values (1834, 'Critical Fours & Null (5 Suits)');
insert into variants values (1835, 'Critical Fours & Muddy Rainbow (6 Suits)');
insert into variants values (1836, 'Critical Fours & Muddy Rainbow (5 Suits)');
insert into variants values (1837, 'Critical Fours & Light Pink (6 Suits)');
insert into variants values (1838, 'Critical Fours & Light Pink (5 Suits)');
insert into variants values (1839, 'Critical Fours & Prism (6 Suits)');
insert into variants values (1840, 'Critical Fours & Prism (5 Suits)');

select * from variants where variant_id = 1353;
select * from variants where variant like 'Syn%' or variant like 'Critical%';
--60
update variants set colors = null where variant like 'Syn%' or variant like 'Critical%';

select * into tags_copy from tags;
alter table tags drop constraint tags_pkey;
alter table tags add primary key(game_id, player, tag);

alter table bugged_games drop constraint bugged_games_pkey;
alter table bugged_games add primary key(game_id, test);

--add odds and evens
select * from variants order by 1;

update variants set variant_id = 18201 where variant_id = 1820;

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1820, 'Odds and Evens & Black (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Black (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1841, 'Odds and Evens & Black (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Black (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1842, 'Odds and Evens & Rainbow (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Rainbow (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1843, 'Odds and Evens & Rainbow (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Rainbow (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1844, 'Odds and Evens & Rainbow (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Rainbow (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1845, 'Odds and Evens & Rainbow (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Rainbow (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1846, 'Odds and Evens & Pink (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Pink (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1847, 'Odds and Evens & Pink (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Pink (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1848, 'Odds and Evens & Pink (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Pink (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1849, 'Odds and Evens & Pink (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Pink (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1850, 'Odds and Evens & White (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'White (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1851, 'Odds and Evens & White (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'White (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1852, 'Odds and Evens & White (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'White (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1853, 'Odds and Evens & White (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'White (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1854, 'Odds and Evens & Brown (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Brown (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1855, 'Odds and Evens & Brown (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Brown (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1856, 'Odds and Evens & Brown (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Brown (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1857, 'Odds and Evens & Brown (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Brown (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1858, 'Odds and Evens & Omni (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Omni (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1859, 'Odds and Evens & Omni (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Omni (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1860, 'Odds and Evens & Omni (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Omni (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1861, 'Odds and Evens & Omni (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Omni (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1862, 'Odds and Evens & Null (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Null (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1863, 'Odds and Evens & Null (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Null (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1864, 'Odds and Evens & Null (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Null (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1865, 'Odds and Evens & Null (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Null (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1866, 'Odds and Evens & Muddy Rainbow (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Muddy Rainbow (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1867, 'Odds and Evens & Muddy Rainbow (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Muddy Rainbow (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1868, 'Odds and Evens & Muddy Rainbow (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Muddy Rainbow (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1869, 'Odds and Evens & Muddy Rainbow (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Muddy Rainbow (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1870, 'Odds and Evens & Light Pink (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Light Pink (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1871, 'Odds and Evens & Light Pink (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Light Pink (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1872, 'Odds and Evens & Light Pink (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Light Pink (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1873, 'Odds and Evens & Light Pink (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Light Pink (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1874, 'Odds and Evens & Prism (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Prism (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1875, 'Odds and Evens & Prism (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Prism (5 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1876, 'Odds and Evens & Prism (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Prism (4 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1877, 'Odds and Evens & Prism (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Prism (3 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1878, 'Odds and Evens & Dark Rainbow (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Rainbow (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1879, 'Odds and Evens & Dark Rainbow (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Rainbow (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1880, 'Odds and Evens & Dark Pink (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Pink (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1881, 'Odds and Evens & Dark Pink (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Pink (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1882, 'Odds and Evens & Gray (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Gray (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1883, 'Odds and Evens & Gray (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Gray (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1884, 'Odds and Evens & Dark Brown (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Brown (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1885, 'Odds and Evens & Dark Brown (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Brown (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1886, 'Odds and Evens & Dark Omni (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Omni (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1887, 'Odds and Evens & Dark Omni (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Omni (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1888, 'Odds and Evens & Dark Null (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Null (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1889, 'Odds and Evens & Dark Null (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Null (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1890, 'Odds and Evens & Cocoa Rainbow (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Cocoa Rainbow (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1891, 'Odds and Evens & Cocoa Rainbow (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Cocoa Rainbow (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1892, 'Odds and Evens & Gray Pink (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Gray Pink (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1893, 'Odds and Evens & Gray Pink (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Gray Pink (5 Suits)';

INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1894, 'Odds and Evens & Dark Prism (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Prism (6 Suits)';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1895, 'Odds and Evens & Dark Prism (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'Dark Prism (5 Suits)';

select * from variants order by 1 desc;

--add funnels
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1896, 'Funnels (6 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = '6 Suits';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1897, 'Funnels (5 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = 'No Variant';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1898, 'Funnels (4 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = '4 Suits';
INSERT INTO variants (variant_id, variant, max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p)
SELECT 1899, 'Funnels (3 Suits)', max_score, suits, special_rank, special_deceptive, special_all_clue_colors, special_all_clue_ranks, special_no_clue_colors, special_no_clue_ranks, colors, eff_2p, eff_34p, eff_5p, eff_6p
FROM variants WHERE variant = '3 Suits';

select * from variants where variant_id = 1;
select * from variants where variant like '%Dual%';
select variant, suits, colors from variants where variant_id > 1901;

delete from variants where variant like 'Funnels &%'
or variant like 'Chimneys%'
or variant like 'Candy%';

select * from variants where variant like 'Funnels%';

ALTER TABLE variants DROP CONSTRAINT variants_pkey;
alter table variants add constraint variants_pkey primary key (variant_id, variant);

ALTER TABLE games ADD CONSTRAINT games_variant_id_variant_fkey FOREIGN KEY (variant_id, variant) REFERENCES variants (variant_id, variant);

select * from variants where variant like 'Odds%';
update games set variant = replace(variant, 'Odds And', 'Odds and');
select * from games;
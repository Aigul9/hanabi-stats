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

create table bugged_games(
    game_id int primary key
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
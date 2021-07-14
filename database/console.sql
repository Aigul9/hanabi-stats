select * from games where game_id = 99104;
select * from games where starting_player is not null;

select * from decks order by seed, card_index;
select distinct seed from decks;

select * from game_actions;

select * from player_notes where game_id = 103429 and player = 'TimeHoodie';

-- delete from player_notes where 1 = 1;
-- delete from game_actions where 1 = 1;
-- delete from games where 1 = 1;

CREATE INDEX games_index_variant_id  ON games (variant);
CREATE INDEX games_index_seed        ON games (seed);

-- ALTER TABLE games ADD CONSTRAINT games_seed_fkey FOREIGN KEY (seed) REFERENCES decks (seed);

select * from games left join decks on games.seed = decks.seed;

ALTER TABLE games ADD COLUMN starting_player integer;

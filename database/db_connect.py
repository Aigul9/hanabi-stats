from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.types import ARRAY

db_name = 'hanabi_db'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'localhost'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
Session = sessionmaker(bind=db)
Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'
    game_id = Column(Integer, primary_key=True)
    num_players = Column(Integer)
    players = Column(ARRAY(String))
    starting_player = Column(Integer)
    variant_id = Column(Integer, ForeignKey('variants.variant_id'))
    variant = Column(String)
    timed = Column(Boolean)
    time_base = Column(Integer)
    time_per_turn = Column(Integer)
    speedrun = Column(Boolean)
    card_cycle = Column(Boolean)
    deck_plays = Column(Boolean)
    empty_clues = Column(Boolean)
    one_extra_card = Column(Boolean)
    one_less_card = Column(Boolean)
    all_or_nothing = Column(Boolean)
    detrimental_characters = Column(Boolean)
    score = Column(Integer)
    num_turns = Column(Integer)
    end_condition = Column(Integer)
    date_time_started = Column(DateTime)
    date_time_finished = Column(DateTime)
    num_games_on_this_seed = Column(Integer)
    tags = Column(String)
    seed = Column(String)

    def __init__(self, game_id, num_players, players, starting_player, variant_id, variant, timed, time_base,
                 time_per_turn, speedrun, card_cycle, deck_plays, empty_clues, one_extra_card, one_less_card,
                 all_or_nothing, detrimental_characters, score, num_turns, end_condition, date_time_started,
                 date_time_finished, num_games_on_this_seed, tags, seed):
        self.game_id = game_id
        self.num_players = num_players
        self.players = players
        self.starting_player = starting_player
        self.variant_id = variant_id
        self.variant = variant
        self.timed = timed
        self.time_base = time_base
        self.time_per_turn = time_per_turn
        self.speedrun = speedrun
        self.card_cycle = card_cycle
        self.deck_plays = deck_plays
        self.empty_clues = empty_clues
        self.one_extra_card = one_extra_card
        self.one_less_card = one_less_card
        self.all_or_nothing = all_or_nothing
        self.detrimental_characters = detrimental_characters
        self.score = score
        self.num_turns = num_turns
        self.end_condition = end_condition
        self.date_time_started = date_time_started
        self.date_time_finished = date_time_finished
        self.num_games_on_this_seed = num_games_on_this_seed
        self.tags = tags
        self.seed = seed


class Card(Base):
    __tablename__ = 'decks'
    seed = Column(String, primary_key=True)
    card_index = Column(Integer, primary_key=True)
    suit_index = Column(Integer)
    rank = Column(Integer)

    def __init__(self, seed, card_index, suit_index, rank):
        self.seed = seed
        self.card_index = card_index
        self.suit_index = suit_index
        self.rank = rank


class GameAction(Base):
    __tablename__ = 'game_actions'
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    turn = Column(Integer, primary_key=True)

    # 0 - play, 1 - discard, 2 - color clue, 3 - rank clue, 4 - game over
    action_type = Column(Integer)

    # If a play or a discard, corresponds to the order of the the card that was played/discard
    # If a clue, corresponds to the index of the player that received the clue
    # If a game over, corresponds to the index of the player that caused the game to end
    target = Column(Integer)

    # If a play or discard, then 0 (as NULL)
    # If a color clue, then 0 if red, 1 if yellow, etc.
    # If a rank clue, then 1 if 1, 2 if 2, etc.
    # If a game over, then the value corresponds to the 'endCondition' values
    value = Column(Integer)

    def __init__(self, game_id, turn, action_type, target, value):
        self.game_id = game_id
        self.turn = turn
        self.action_type = action_type
        self.target = target
        self.value = value


class PlayerNotes(Base):
    __tablename__ = 'player_notes'
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    player = Column(String, primary_key=True)
    notes = Column(ARRAY(String))

    def __init__(self, game_id, player, notes):
        self.game_id = game_id
        self.player = player
        self.notes = notes


class Variant(Base):
    __tablename__ = 'variants'
    variant_id = Column(Integer, primary_key=True)
    variant = Column(String)
    max_score = Column(Integer)
    max_score_2p = Column(Integer)
    max_score_3p = Column(Integer)
    max_score_4p = Column(Integer)
    max_score_5p = Column(Integer)
    max_score_6p = Column(Integer)
    suits = Column(ARRAY(String))
    special_rank = Column(Integer)
    special_deceptive = Column(Boolean)
    special_all_clue_colors = Column(Boolean)
    special_all_clue_ranks = Column(Boolean)
    special_no_clue_colors = Column(Boolean)
    special_no_clue_ranks = Column(Boolean)
    colors = Column(ARRAY(String))

    def __init__(self,
                 variant_id,
                 variant,
                 max_score,
                 max_score_2p,
                 max_score_3p,
                 max_score_4p,
                 max_score_5p,
                 max_score_6p,
                 suits,
                 special_rank,
                 special_deceptive,
                 special_all_clue_colors,
                 special_all_clue_ranks,
                 special_no_clue_colors,
                 special_no_clue_ranks,
                 colors):
        self.variant_id = variant_id
        self.variant = variant
        self.max_score = max_score
        self.max_score_2p = max_score_2p
        self.max_score_3p = max_score_3p
        self.max_score_4p = max_score_4p
        self.max_score_5p = max_score_5p
        self.max_score_6p = max_score_6p
        self.suits = suits
        self.special_rank = special_rank
        self.special_deceptive = special_deceptive
        self.special_all_clue_colors = special_all_clue_colors
        self.special_all_clue_ranks = special_all_clue_ranks
        self.special_no_clue_colors = special_no_clue_colors
        self.special_no_clue_ranks = special_no_clue_ranks
        self.colors = colors


class CardAction(Base):
    __tablename__ = 'card_actions'
    card_index = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    # Muddy Rainbow
    card_suit = Column(String)
    card_rank = Column(Integer)
    player = Column(String)
    turn_drawn = Column(Integer)
    # play, discard
    action_type = Column(String)
    turn_action = Column(Integer)

    def __init__(self, card_index, game_id, card_suit, card_rank, player,
                 turn_drawn, action_type, turn_action):
        self.card_index = card_index
        self.game_id = game_id
        self.card_suit = card_suit
        self.card_rank = card_rank
        self.player = player
        self.turn_drawn = turn_drawn
        self.action_type = action_type
        self.turn_action = turn_action


class Clue(Base):
    __tablename__ = 'clues'
    turn_clued = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    # Purple, 5
    clue = Column(String)
    # color, rank
    clue_type = Column(String)
    clue_giver = Column(String)
    clue_receiver = Column(String)

    def __init__(self, turn_clued, game_id, clue, clue_type, clue_giver, clue_receiver):
        self.turn_clued = turn_clued
        self.game_id = game_id
        self.clue = clue
        self.clue_type = clue_type
        self.clue_giver = clue_giver
        self.clue_receiver = clue_receiver


Base.metadata.create_all(db)
session = Session()
session.commit()

# delete from games where 1 = 1

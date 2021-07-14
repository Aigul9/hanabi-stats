from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Boolean
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
    players = Column(ARRAY(String))
    variant = Column(String)
    timed = Column(Boolean)
    time_base = Column(Integer)
    time_per_turn = Column(Integer)
    seed = Column(String)

    def __init__(self, game_id, players, variant, timed, time_base, time_per_turn, seed):
        self.game_id = game_id
        self.players = players
        self.variant = variant
        self.timed = timed
        self.time_base = time_base
        self.time_per_turn = time_per_turn
        self.seed = seed


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
    # game = relationship('Game', backref=backref('game_actions', uselist=False))

    def __init__(self, game_id, turn, action_type, target, value):
        self.game_id = game_id
        self.turn = turn
        self.action_type = action_type
        self.target = target
        self.value = value
        # self.game = game


class PlayerNotes(Base):
    __tablename__ = 'player_notes'
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    player = Column(String)
    notes = Column(ARRAY(String))
    # game = relationship('Game', backref=backref('player_notes', uselist=False))

    def __init__(self, game_id, player, notes):
        self.game_id = game_id
        self.player = player
        self.notes = notes
        # self.game = game


Base.metadata.create_all(db)
session = Session()
game_582461 = Game(
    582461,
    [
        'Valetta6789',
        'melwen',
        'Lanvin',
        'Zamiel'
    ],
    'Rainbow-Ones & Brown (4 Suits)',
    True,
    90,
    15,
    'p4v304s2'
)

session.add(game_582461)
session.commit()
session.close()

games = session.query(Game).all()
for g in games:
    print(g.players)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import py.utils as ut
from database.db_schema import Base, Game, GameAction, PlayerNotes


db_name = 'hanabi_db'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'localhost'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
Session = sessionmaker(bind=db)
Base.metadata.create_all(db)
session = Session()


path = '../temp/games_dumps/'
files = ut.files_in_dir(path)


def open_as_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = {}
        for line in file.readlines():
            try:
                line_dict = json.loads(line.rstrip())
                data[line_dict['id']] = line_dict
            except json.decoder.JSONDecodeError:
                print(line)
                exit()
        return data


games = {}
for f in files:
    print(f)
    games = games | open_as_json(f'{path}{f}')

for g_id, g in games.items():
    # print(g)
    try:
        opt = g['options']
        timed = opt['timed']
        time_base = opt['timeBase']
        time_per_turn = opt['timePerTurn']
        try:
            var = opt['variant']
        except KeyError:
            var = None
    except KeyError:
        var = None
        timed = None
        time_base = None
        time_per_turn = None
    actions = g['actions']
    game = Game(
        g_id,
        g['players'],
        var,
        timed,
        time_base,
        time_per_turn,
        g['seed']
    )
    for i in range(len(actions)):
        action = GameAction(
            g_id,
            i,
            actions[i]['type'],
            actions[i]['target'],
            actions[i]['value'],
        )
        session.add(action)
    try:
        game_notes = g['notes']
        for i in range(len(game_notes)):
            player_notes = PlayerNotes(
                g_id,
                g['players'][i],
                game_notes[i]
            )
            session.add(player_notes)
    except KeyError:
        pass
    session.add(game)

session.commit()
session.close()

# delete from games where 1 = 1

import json
import py.utils as ut
import database.db_load as d


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


def load_games():
    data = {}
    for f in files:
        print(f)
        data = data | open_as_json(f'{path}{f}')
    return data


path = '../temp/games_dumps/'
files = ut.files_in_dir(path)

games = load_games()
for g in games.values():
    d.load_deck(g)
    # d.load_game(g)
    # d.load_actions(g)
    # d.load_notes(g)

d.session.commit()
d.session.close()

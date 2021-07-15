import json
import logging

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


def load_games(path):
    files = ut.files_in_dir(path)
    data = {}
    for f in files:
        print(f)
        data = data | open_as_json(f'{path}{f}')
    return data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

hanabi_players = ut.open_file('../output/hanabi_players.txt')
for p in hanabi_players:
    logger.info(p)
    try:
        stats = ut.open_stats(p)
    except json.decoder.JSONDecodeError:
        logger.error(p)
        continue
    for s in stats:
        d.update_game(s)
    d.session.commit()

# stats = ut.open_stats('Livia')
# for s in stats:
#     d.update_game(s)

# path = '../temp/games_dumps/'
#
# games = load_games(path)
# for g in games.values():
    # d.load_column(g)
    # d.load_deck(g)
    # d.load_game(g)
    # d.load_actions(g)
    # d.load_notes(g)

d.session.close()

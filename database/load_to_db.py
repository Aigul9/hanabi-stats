import json

from sqlalchemy import func, and_, false

import py.utils as u
import database.db_load as d
from py.utils import logger
from database.db_connect import session, Game, Slot


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
    files = u.files_in_dir(path)
    data = {}
    for f in files:
        print(f)
        data = data | open_as_json(f'{path}{f}')
    return data


def load_from_files(all_games):
    for g in all_games.values():
        s = u.open_stats_by_game_id(g['players'][0], g['id'])
        d.load_deck(g)
        d.load_game(g, s)
        # d.load_game_empty(g)
        d.load_actions(g)
        d.load_notes(g)
        d.session.commit()
        logger.info(g['id'])
        
        
def load_cards(all_games):
    for g in all_games:
        d.update_action_types(g)
        # d.load_card_actions_and_clues(g)
        d.session.commit()
        logger.info(g.game_id)


def load_slots(all_games):
    for g in all_games:
        d.load_slots(g)
        d.session.commit()
        logger.info(g.game_id)

# dumps = '../temp/games_dumps/'
# 
# games = load_games(dumps)


last_id = d.session.query(func.max(Slot.game_id)).scalar()
games = session.query(
    Game.game_id,
    Game.num_players,
    Game.one_less_card,
    Game.one_extra_card
) \
    .filter(
    and_(
        Game.card_cycle == false(),
        Game.game_id > last_id
    ))\
    .order_by(Game.game_id)\
    .all()

load_slots(games)
d.session.close()

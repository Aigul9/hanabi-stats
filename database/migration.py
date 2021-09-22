from datetime import datetime
from json.decoder import JSONDecodeError

import requests
from sqlalchemy import func

from database.db_connect import Game
from py.utils import logger
import py.utils as u
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
# last_id = 627743
logger.info(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
logger.info(f'last id: {last_id}')
req_session = requests.Session()
histories = {}
while True:
    g_id = last_id + 1
    g = u.export_game(g_id, req_session)
    if g != {}:
        player = g['players'][0]
        if player in histories.keys():
            s = u.open_stats_by_game_id(histories[player], g_id)
        else:
            try:
                response = u.open_stats(player, req_session)
            except JSONDecodeError:
                logger.error(f'error: {g_id}')
                last_id += 1
                continue
            s = u.open_stats_by_game_id(response, g_id)
            histories[player] = response
        deck = d.load_deck(g)
        db_game = d.load_game(g, s)
        game_actions = d.load_actions(g)
        d.load_notes(g)
        if not db_game.detrimental_characters:
            d.load_card_actions_and_clues(db_game, game_actions, deck)
        last_id += 1
        d.load_slots(db_game)
        d.session.commit()
    else:
        d.session.close()
        logger.error(f'end: {g_id}')
        logger.info(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        break

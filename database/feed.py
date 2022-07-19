from datetime import datetime

import requests
from sqlalchemy import func

from database.db_connect import Game, session
from py.utils import logger
import py.utils as u
import database.db_load as d


last_id_db = session.query(func.max(Game.game_id)).scalar()  # start of the loop
# last_id_db = 726704
LAST_ID_SITE = 810239  # end of the loop
logger.info(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\tstart:\t{last_id_db}')
req_session = requests.Session()
histories = {}  # cache for players' histories

while last_id_db <= LAST_ID_SITE:
    g_id = last_id_db + 1
    g = u.export_game(g_id, req_session)

    if g == {}:  # if game does not exist
        last_id_db += 1
        continue

    if len(g['players']) == 0:
        logger.error(g_id)
        last_id_db += 1
        continue

    player = g['players'][0]

    if player in histories.keys():
        s = u.open_stats_by_game_id(histories[player], g_id)
    else:
        response = u.open_stats_from_id_start(player, last_id_db, req_session)
        s = u.open_stats_by_game_id(response, g_id)
        histories[player] = response

    deck = d.load_deck(g)
    db_game = d.load_game(g, s)
    game_actions = d.load_actions(g)
    d.load_notes(g)
    d.load_tags(s)

    if not db_game.detrimental_characters:  # since they have different logic, they are just skipped
        d.load_card_actions_and_clues(db_game, game_actions, deck)

    last_id_db += 1
    d.load_slots(db_game)
    d.session.commit()

        
d.session.close()
logger.info(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\tfinish:\t{last_id_db}')

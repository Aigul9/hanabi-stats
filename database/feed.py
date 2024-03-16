import json

import requests
from sqlalchemy import func

from database.db_connect import Game, session
from py.utils import logger
import py.utils as u
import database.db_load as d

last_id_db = session.query(func.max(Game.game_id)).scalar()  # start of the loop
req_session = requests.Session()
histories = {}  # cache for players' histories
counter = 0  # number of consecutive 404 games
MAX_COUNTER = 5000

while True:
    g_id = last_id_db + 1
    g = u.export_game(g_id, req_session)

    if g == {}:  # if game does not exist
        if counter > MAX_COUNTER:
            break

        last_id_db += 1
        counter += 1
        continue
        # break

    if len(g['players']) == 0:
        logger.error(g_id)
        last_id_db += 1
        continue

    is_success = False
    player_idx = 0
    while not is_success and player_idx < len(g['players']):
        player = g['players'][player_idx]
        if player in histories.keys():
            try:
                s = u.open_stats_by_game_id(histories[player], g_id)
                is_success = True
                break
            except IndexError:
                logger.error("The game does not exist in player's local history")
                pass

        try:
            response = u.open_stats_from_id_start(player, last_id_db, req_session)
            s = u.open_stats_by_game_id(response, g_id)
            histories[player] = response
            is_success = True
        except (IndexError, json.decoder.JSONDecodeError):
            logger.error("Can't read the stats from api")
            player_idx += 1

    if not is_success:
        logger.error(f'====={g_id}: PLAYERS NOT FOUND====')
        last_id_db += 1
        continue

    deck = d.load_deck(g)
    db_game = d.load_game(g, s)
    game_actions = d.load_actions(g)
    d.load_notes(g)
    # d.load_tags(s)

    if not db_game.detrimental_characters:  # since they have different logic, they are just skipped
        d.load_card_actions_and_clues(db_game, game_actions, deck)

    last_id_db += 1
    d.load_slots(db_game)
    d.session.commit()
    counter = 0

d.session.close()

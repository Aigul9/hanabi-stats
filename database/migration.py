from sqlalchemy import func

from database.db_connect import Game
from py.utils import logger
import py.utils as u
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
# last_id = 612472
logger.info(f'last id: {last_id}')
while True:
    g_id = last_id + 1
    g = u.export_game(g_id)
    if g != {}:
        logger.info(g_id)
        s = u.open_stats_by_game_id(g['players'][0], g_id)
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
        last_id += 1
        logger.error(f'skip: {last_id}')
        d.session.close()
        break

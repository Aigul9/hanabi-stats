from sqlalchemy.sql import func
from database.db_connect import Game
from py.utils import logger
import py.utils as u
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
logger.info(f'last id: {last_id}')
while True:
    g_id = last_id + 1
    g = u.export_game(g_id)
    if g != {}:
        logger.info(g_id)
        s = u.open_stats_by_game_id(g['players'][0], g_id)
        d.load_deck(g)
        db_game = d.load_game(g, s)
        # d.load_empty_game(g)
        d.load_actions(g)
        d.load_notes(g)
        d.load_card_actions_and_clues(db_game)
        d.update_misplays(db_game)
        last_id += 1
        d.session.commit()
    else:
        d.session.close()
        break

from sqlalchemy.sql import func
from database.db_connect import Game
import py.utils as ut
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
# last_id = 2906
print('last_id:', last_id)
while True:
    g_id = last_id + 1
    g = ut.export_game(g_id)
    if g != {}:
        s = ut.open_stats_by_game_id(g['players'][0], g_id)
        d.load_deck(g)
        d.load_game(g, s)
        d.load_actions(g)
        d.load_notes(g)
        last_id += 1
        d.session.commit()
    else:
        d.session.close()
        break

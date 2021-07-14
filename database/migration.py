from sqlalchemy.sql import func
from database.db_schema import Game
import py.utils as ut
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
print('last_id:', last_id)
while True:
    g = ut.export_game(last_id + 1)
    if g != {}:
        d.load_deck(g)
        d.load_game(g)
        d.load_actions(g)
        d.load_notes(g)
        last_id += 1
    else:
        d.session.commit()
        d.session.close()
        break

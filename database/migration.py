from sqlalchemy.sql import func
from database.db_schema import Game
import py.utils as ut
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar()
print('last_id:', last_id)
while True:
    g = ut.export_game(last_id + 1)
    if g != {}:
        d.load(g['id'], g)
        last_id += 1
    else:
        d.session.commit()
        d.session.close()
        break

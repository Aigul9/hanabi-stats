from sqlalchemy.sql import func
from database.db_schema import Game
import py.utils as ut
import database.db_load as d


last_id = d.session.query(func.max(Game.game_id)).scalar() + 1
print('last_id:', last_id)
while True:
    g = ut.export_game(last_id)
    if g != {}:
        print(last_id)
        last_id += 1
        d.load(g['id'], g)
    else:
        d.session.commit()
        d.session.close()
        exit()

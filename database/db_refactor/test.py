import database.db_load as d
import py.utils as u
from database.db_connect import session, Card

ids = [
    31452,
    52672,
    125376,
    165789,
    84922,
    321112,
    549167,
    553127
]
for g_id in ids:
    g = u.export_game(g_id)
    deck = session.query(Card).filter_by(seed=g['seed']).delete()
    d.load_deck(g)
    d.session.commit()
d.session.close()

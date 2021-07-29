import database.db_load as d
import py.utils as u
from database.db_connect import session, Card, Game

# ids = [
#     410466,
#     345883,
#     403401
# ]
# for g_id in ids:
#     g = u.export_game(g_id)
#     deck = session.query(Card).filter_by(seed=g['seed']).delete()
#     d.load_deck(g)
#     game = session.query(Game).filter(Game.game_id == g_id).first()
#     d.load_card_actions_and_clues(game)
#     d.session.commit()
d.load_variant('test', 9999)
d.session.commit()
d.session.close()

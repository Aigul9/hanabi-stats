import database.db_load as d
import py.utils as u

g = u.export_game(9107)
d.load_deck(g)
d.session.commit()
d.session.close()

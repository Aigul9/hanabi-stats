import database.load_from_file as load
import database.db_load as d


games = load.load_games()
for g_id, g in games.items():
    d.load(g_id, g)

d.session.commit()
d.session.close()

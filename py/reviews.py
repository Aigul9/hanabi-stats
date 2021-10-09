import csv

from database.db_connect import session, Game

games = session.query(Game) \
    .filter(Game.game_id > 640420) \
    .order_by(Game.game_id) \
    .all()

with open('../output/rev2.tsv', 'w', encoding='utf-8', newline='') as file:
    w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')

    for i in range(len(games) - 1):
        game = games[i]
        game_id = game.game_id
        players = game.players
        finish = game.date_time_finished
        ids = []
        for p in players:
            g_id = session.query(Game.game_id) \
                .filter(Game.players.any(p)) \
                .filter(Game.game_id > game_id) \
                .order_by(Game.game_id) \
                .first()
            if g_id is None:
                continue
            ids.append(g_id[0])
        if len(ids) == 0:
            continue
        start = session.query(Game.date_time_started) \
            .filter(Game.game_id == min(ids)) \
            .scalar()
        w.writerow([game_id, start - finish])

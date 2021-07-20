import csv

import py.utils as u
from database.db_connect import session, Game, GameAction, Variant


users = ['Dr_Kakashi', 'Valetta6789', 'Lanvin']
# [game_id, player_count, clues]
results = {k: [] for k in users}
for user in users:
    games = session.query(Game) \
        .join(Variant) \
        .filter(Game.players.any(user)) \
        .filter(Game.score == Variant.max_score) \
        .all()
    for g in games:
        game_id = g.game_id
        print(game_id)
        players = g.players
        players_count = len(players)
        players = (players[g.starting_player:] + players[:g.starting_player])
        actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
        clues = {k: 0 for k in players}
        for i in range(len(actions)):
            if u.is_clued(actions[i]):
                clues[players[i % players_count]] += 1
        max_users = [k for k, v in clues.items() if v == max(clues.values())]
        if len(max_users) == 1 and max_users[0] == user:
            results[user].append([game_id, players_count, clues[user]])

    for c in range(2, 7):
        with open(f'../output/clues/{user}_clues_{c}p.tsv', 'a', encoding='utf-8', newline='') as file:
            w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
            w.writerow(['Game id', 'Player count', 'Number of clues'])
            data = sorted([v for v in results[user] if v[1] == c], key=lambda x: -x[2])
            for r in data:
                w.writerow([*r])

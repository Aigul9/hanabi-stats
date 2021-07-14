import csv

import py.utils as ut
from database.db_connect import session
from database.db_schema import Game, Card, GameAction, PlayerNotes


users = ['Dr_Kakashi']
# [game_id, player_count, clues]
results = {k: [] for k in users}
for u in users:
    stats = ut.open_stats(u)
    for s in stats:
        # game_id = 140017
        game_id = s['id']
        print(game_id)
        players = session.query(Game.players).filter(Game.game_id == game_id).scalar()
        actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
        player_count = len(players)
        clues = {k: 0 for k in players}
        for i in range(len(actions)):
            if ut.is_clued(actions[i]):
                clues[players[i % player_count]] += 1
        max_users = [k for k, v in clues.items() if v == max(clues.values())]
        if len(max_users) == 1 and max_users[0] in results:
            results[max_users[0]].append([game_id, player_count, clues[max_users[0]]])
        # print(clues)
        # print(results)
# print(results)
results = sorted([i for v in results.values() for i in v if i[1] == 3], key=lambda x: -x[2])
with open(f'../output/Dr_Kakashi_clues.tsv', 'a', encoding='utf-8', newline='') as file:
    w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
    w.writerow(['Game id', 'Player count', 'Number of clues'])
    for r in results:
        w.writerow([*r])

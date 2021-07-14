import csv

import py.utils as ut
from database.db_connect import session
from database.db_schema import Game, GameAction


users = ['Dr_Kakashi']
# [game_id, player_count, clues]
results = {k: [] for k in users}
for u in users:
    stats = ut.open_stats(u)
    for s in stats:
        # for s in [99104]:
        game_id = s['id']
        # game_id = s
        print(game_id)
        players, starting_player = session.query(Game.players, Game.starting_player).filter(Game.game_id == game_id).first()
        players_count = len(players)
        if starting_player is not None:
            players = (players[starting_player:] + players[:starting_player])
        actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
        clues = {k: 0 for k in players}
        for i in range(len(actions)):
            if ut.is_clued(actions[i]):
                clues[players[i % players_count]] += 1
        max_users = [k for k, v in clues.items() if v == max(clues.values())]
        if len(max_users) == 1 and max_users[0] == u:
            results[u].append([game_id, players_count, clues[u]])


for c in range(2, 7):
    with open(f'../output/Dr_Kakashi_clues_{c}p.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Game id', 'Player count', 'Number of clues'])
    data = sorted([i for v in results.values() for i in v if i[1] == c], key=lambda x: -x[2])
    for r in data:
        w.writerow([*r])

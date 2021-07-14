import operator

import py.utils as ut


users = ['Dr_Kakashi']
# [game_id, player_count, clues]
results = {k: [] for k in users}
for u in users:
    stats = ut.open_stats(u)
    for s in stats:
        # game_id = 140017
        game_id = s['id']
        game = games[game_id]
        players = game['players']
        actions = game['actions']
        player_count = len(players)
        clues = {k: 0 for k in players}
        for i in range(len(actions)):
            if ut.is_clued(actions[i]):
                clues[players[i % player_count]] += 1
        max_user = max(clues.items(), key=operator.itemgetter(1))[0]
        if max_user in results:
            results[max_user].append([game_id, player_count, clues[max_user]])
        # print(clues)
        # print(results)
print(results)

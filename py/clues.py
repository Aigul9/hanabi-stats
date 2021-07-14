import json
import operator

import py.utils as ut


def open_as_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = {}
        for line in file.readlines():
            line_dict = json.loads(line.rstrip())
            data[line_dict['id']] = line_dict
        return data


path = '../temp/games_dumps/'
files = ut.files_in_dir(path)
games = {}
for f in files:
    games = games | open_as_json(f'{path}{f}')
    print(f)
# print(games.keys())
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

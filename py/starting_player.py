import py.utils as ut
from itertools import groupby


with open('../input/list_of_players_notes.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


# with open('../output/misc/all_games.tsv', 'r') as f:
#     all_games = [line.rstrip().split('\t') for line in f.readlines()]


with open('../output/misc/starting_player_logs.txt', 'r') as f:
    games = [line.rstrip().split(', ') for line in f.readlines()]


# # games = []
# for g in all_games:
#     game_id = g[0]
#     game = ut.export_game(game_id)
#     # print(game['players'][g[1]])
#     starting_player = game['players'][int(g[1])]
#     g[1] = starting_player
#     print(g)
#     # games.append(game)
# # print(games)


# test = [
#     {'id': 581699, 'sp': 'Lel0uch', 'result': 'loss'},
#     {'id': 581689, 'sp': 'Lel0uch', 'result': 'win'},
#     {'id': 581680, 'sp': 'Valetta6789', 'result': 'loss'}
# ]

# print([r for r in games if r[1] == 'Zamiel'])
players = set([r[1] for r in games])
grouped_stats = {}
for u in players:
    if u in users:
        group = [r for r in games if r[1] == u]
        g_len = len(group)
        group_wins = len([r for r in group if r[2] == 'win'])
        grouped_stats[u] = [ut.p(group_wins, g_len), g_len]
grouped_stats = {k: v for k, v in sorted(grouped_stats.items(), key=lambda x: -x[1][0])}

ut.save('starting_player_rate', grouped_stats, ['Player', 'Rate', 'Total'])

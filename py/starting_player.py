import py.utils as ut
import py.calc as c


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

players = set([r[1] for r in games])
grouped_stats = {}
for u in players:
    if u in users:
        group = [r for r in games if r[1] == u]
        stats = ut.clear_2p(ut.clear_speedruns(ut.open_stats(u)))
        # num games overall
        s_len = len(stats)
        # num wins overall
        total_wins = c.get_wins(stats)
        # num games going first
        g_len = len(group)
        # num wins going first
        group_wins = len([r for r in group if r[2] == 'win'])
        formula = round((group_wins / g_len) / (total_wins / s_len), 2)
        grouped_stats[u] = [formula, group_wins, g_len, total_wins, s_len]
grouped_stats = {k: v for k, v in sorted(grouped_stats.items(), key=lambda x: -x[1][0])}

ut.save('starting_player_rate_2', grouped_stats, [
    'Player',
    'Ratio',
    'Num wins going first',
    'Num games going first',
    'Num wins overall',
    'Num games overall'
])

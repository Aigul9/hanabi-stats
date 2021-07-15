import py.utils as ut
import py.calc as c

# TODO: refactor using db
with open('../input/list_of_players_notes.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


with open('../output/misc/starting_player_logs.txt', 'r') as f:
    games = [line.rstrip().split(', ') for line in f.readlines()]


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

ut.save('winrate/alice/starting_player_upd', grouped_stats, [
    'Player',
    'Ratio',
    'Num wins going first',
    'Num games going first',
    'Num wins overall',
    'Num games overall'
])

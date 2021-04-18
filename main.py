import csv
import time
import py.parsing as prs
import py.players as pl
import py.calc as c
from datetime import datetime


def r(num):
    return str(num).replace('.', ',')


start = time.time()
with open('../input/all_players.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

results = {}
for u in users:
    # parsing
    history_table = prs.get_history_table(u)
    items = prs.get_stats(history_table)
    prs.save_stats(items, u)
    prs.save_list_of_players(items, u)
    # set of players
    pl.save_players_list(pl.create_players_set(u), u)
    totals, totals_easy, totals_null, totals_sd, totals_dd = c.get_all_stats(u)
    results[u] = c.get_all_stats(u)

print('Data is generated.')

with open(f'../output/all_stat_{datetime.timestamp(datetime.now())}.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Username', 'Type', 'W(%)', 'L(%)', 'W(#)', 'L(#)',
                'W(%, 2p)', 'L(%, 2p)', 'W(#, 2p)', 'L(#, 2p)',
                'W(%, 3p+)', 'L(%, 3p+)', 'W(#, 3p+)', 'L(#, 3p+)'])
    for k, v in results.items():
        for k1, t in v.items():
            w.writerow([
                k,
                k1,
                # r(t['total_p'][0]),
                t['total_p'][0],
                # r(t['total_p'][1]),
                t['total_p'][1],
                t['total_c'][0],
                t['total_c'][1],
                # r(t['total_2p_p'][0]),
                t['total_2p_p'][0],
                # r(t['total_2p_p'][1]),
                t['total_2p_p'][1],
                t['total_2p_c'][0],
                t['total_2p_c'][1],
                # r(t['total_3p_p'][0]),
                t['total_3p_p'][0],
                # r(t['total_3p_p'][1]),
                t['total_3p_p'][1],
                t['total_3p_c'][0],
                t['total_3p_c'][1]]
            )

print('Time spent (in min):', round((time.time() - start) / 60, 2))

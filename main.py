import csv
import time
import py.parsing as prs
import py.players as pl
import py.calc as c
import py.players_most_wl as wl
from datetime import datetime


def r(num):
    return str(num).replace('.', ',')


def save_to_tsv(filename, data):
    with open(f'../output/{filename}.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            'Username', 'Type',
            'W/L(%)', 'W(%)', 'L(%)', 'W(#)', 'L(#)',
            'W/L(%, 2p)', 'W(%, 2p)', 'L(%, 2p)', 'W(#, 2p)', 'L(#, 2p)',
            'W/L(%, 3p)','W(%, 3p+)', 'L(%, 3p+)', 'W(#, 3p+)', 'L(#, 3p+)']
        )
        for k, v in data.items():
            for k1, t in v.items():
                w.writerow([
                    k,
                    k1,
                    # r(t['total_p'][0]),
                    t['total_p'][2],
                    t['total_p'][0],
                    # r(t['total_p'][1]),
                    t['total_p'][1],
                    t['total_c'][0],
                    t['total_c'][1],
                    # r(t['total_2p_p'][0]),
                    t['total_2p_p'][2],
                    t['total_2p_p'][0],
                    # r(t['total_2p_p'][1]),
                    t['total_2p_p'][1],
                    t['total_2p_c'][0],
                    t['total_2p_c'][1],
                    # r(t['total_3p_p'][0]),
                    t['total_3p_p'][2],
                    t['total_3p_p'][0],
                    # r(t['total_3p_p'][1]),
                    t['total_3p_p'][1],
                    t['total_3p_c'][0],
                    t['total_3p_c'][1]]
                )


def save_wr(filename, data):
    with open(f'../output/highest_wr_{filename}.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'WR', 'Total games'])
        for k, v in sorted(data.items(), key=lambda item: item[1]['Totals']['total_p'], reverse=True):
            w.writerow([
                k,
                v['Totals']['total_p'][0],
                v['Totals']['total_c'][2]
            ])


start = time.time()
with open('../input/list_of_players.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

results = {}
results_var = {}
results_var_not = {}
for u in users:
    # # parsing
    # history_table = prs.get_history_table(u)
    # items = prs.get_stats(history_table)
    # prs.save_stats(items, u)
    # prs.save_list_of_players(items, u)
    # # set of players
    # pl.save_players_list(pl.create_players_set(u), u)
    results[u] = c.get_all_stats(u, 'all')
    results_var[u] = c.get_all_stats(u, 'bga')
    results_var_not[u] = c.get_all_stats(u, 'not bga')
    # # group by players
    # players_list = wl.get_players_list(u)
    # players_dict = wl.get_players_dict(u, players_list)
    # wl.save_players_dict(u, players_dict)


print('Data is generated.')

save_to_tsv(f'all_stats_{datetime.timestamp(datetime.now())}', results)
save_to_tsv('up_to_date_stats', results)
save_wr('all', results)
save_wr('bga', results_var)
save_wr('not_bga', results_var_not)

print('Time spent (in min):', round((time.time() - start) / 60, 2))

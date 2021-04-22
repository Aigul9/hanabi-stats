import csv
import time
import math
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
            'W/L(%, 3p)', 'W(%, 3p+)', 'L(%, 3p+)', 'W(#, 3p+)', 'L(#, 3p+)']
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
        w.writerow(['Username', 'W(%)', 'Total games'])
        for k, v in sorted(data.items(), key=lambda item: item[1]['Totals']['total_p'], reverse=True):
            w.writerow([
                k,
                v['Totals']['total_p'][0],
                v['Totals']['total_c'][2]
            ])


def save_ranking(data):
    with open('../output/rank.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'Rank', 'Seek', 'Hide'])
        for k, v in data.items():
            try:
                u_tops = rank_all_players[k]
            except KeyError:
                u_tops = []
            list_top = []
            list_bottom = []
            for pl in v[1]:
                list_top.append(f'{pl} ({round(u_tops[0][pl]["wl"])}%)')
            for pl in v[2]:
                list_bottom.append(f'{pl} ({round(u_tops[1][pl]["wl"])}%)')
            list_top = ['none'] if len(list_top) == 0 else list_top
            list_bottom = ['none'] if len(list_bottom) == 0 else list_bottom
            w.writerow([
                k,
                v[0],
                ', '.join(list_top),
                ', '.join(list_bottom)
            ])


def assign_weights(username, tb_list, global_type):
    for pl in tb_list:
        if pl not in global_ranking:
            global_ranking[pl] = []
            global_ranking[pl] = [0, [], []]
        if global_type == 'top':
            global_ranking[pl][0] += len(tb_list) - list(tb_list.keys()).index(pl)
            global_ranking[username][1].append(pl)
        elif global_type == 'bottom':
            global_ranking[pl][0] -= list(tb_list.keys()).index(pl) + 1
            global_ranking[username][2].append(pl)


def global_sort(global_list):
    return {k: v for k, v in sorted(global_list.items(), key=lambda item: (-item[1][0]))}


start = time.time()
print('Start time:', datetime.now())
with open('../input/list_of_players.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

results = {}
results_var = {}
results_var_not = {}
global_ranking = {k: [0, [], []] for k in users}
top = 5
rank_all_players = {k: [] for k in users}
for u in users:
    # # parsing
    # history_table = prs.get_history_table(u)
    # items = prs.get_stats(history_table)
    # prs.save_stats(items, u)
    # prs.save_list_of_players(items, u)
    # # set of players
    # pl.save_players_list(pl.create_players_set(u), u)
    # results[u] = c.get_all_stats(u, 'all')
    # results_var[u] = c.get_all_stats(u, 'bga')
    # results_var_not[u] = c.get_all_stats(u, 'non speedrun')
    # group by players
    players_list = wl.get_players_list(u)
    # players_dict = wl.get_players_dict(u, players_list)
    # wl.save_players_dict(u, players_dict)
    # get top 10
    list_for_tops = wl.get_overall_wr(u, players_list)
    mi = math.ceil(len(list_for_tops) / 2)
    first_half = dict(list(list_for_tops.items())[:mi])
    second_half = dict(list(list_for_tops.items())[mi:])
    try:
        if len(list_for_tops) % 2 != 0:
            wl_prev = list_for_tops[list(list_for_tops)[mi - 2]]['wl']
            p_cur = list(list_for_tops)[mi - 1]
            wl_cur = list_for_tops[p_cur]['wl']
            wl_next = list_for_tops[list(list_for_tops)[mi]]['wl']
            if wl_prev - wl_cur > wl_cur - wl_next:
                del first_half[p_cur]
                second_half[p_cur] = list_for_tops[p_cur]
    except IndexError:
        pass
    list_top_n = wl.get_top_n(top, first_half)
    list_bottom_n = wl.get_bottom_n(top, second_half)
    rank_all_players[u] = [list_top_n, list_bottom_n]
    assign_weights(u, list_top_n, 'top')
    assign_weights(u, list_bottom_n, 'bottom')

print('Data is generated.')

save_to_tsv(f'all_stats_{datetime.timestamp(datetime.now())}', results)
save_to_tsv('up_to_date_stats', results)
save_wr('all', results)
save_wr('bga', results_var)
save_wr('non_speedrun', results_var_not)

save_ranking(global_sort(global_ranking))

print('End time:', datetime.now())
print('Time spent (in min):', round((time.time() - start) / 60, 2))

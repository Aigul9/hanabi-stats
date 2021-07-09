import csv
import time
import math
import logging
import py.utils as ut
import py.calc as c
import py.purples as purples
import py.players_most_wl as wl
import py.players as pls
from datetime import datetime
from matplotlib import pyplot as plt


def save_to_tsv(filename, data):
    with open(f'output/{filename}.tsv', 'w', newline='') as file:
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
                    t['total_p'][2],
                    t['total_p'][0],
                    t['total_p'][1],
                    t['total_c'][0],
                    t['total_c'][1],
                    t['total_2p_p'][2],
                    t['total_2p_p'][0],
                    t['total_2p_p'][1],
                    t['total_2p_c'][0],
                    t['total_2p_c'][1],
                    t['total_3p_p'][2],
                    t['total_3p_p'][0],
                    t['total_3p_p'][1],
                    t['total_3p_c'][0],
                    t['total_3p_c'][1]]
                )


def save_wr(filename, data):
    with open(f'output/wr/highest_wr_{filename}.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'W(%)', 'Total games'])
        for k, v in sorted(data.items(), key=lambda item: item[1]['Totals']['total_p'], reverse=True):
            w.writerow([
                k,
                v['Totals']['total_p'][0],
                v['Totals']['total_c'][2]
            ])


def save_ranking(data):
    with open('output/rank/rank_avg.tsv', 'w', newline='') as file:
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
            if len(list_top) == 0 or len(list_bottom) == 0:
                continue
            # list_top = ['none'] if len(list_top) == 0 else list_top
            # list_bottom = ['none'] if len(list_bottom) == 0 else list_bottom
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
            global_ranking[pl] = [0, [], [], 0]
        if global_type == 'top':
            global_ranking[pl][0] += len(tb_list) - list(tb_list.keys()).index(pl)
            global_ranking[username][1].append(pl)
            global_ranking[pl][3] += 1
        elif global_type == 'bottom':
            global_ranking[pl][0] -= list(tb_list.keys()).index(pl) + 1
            global_ranking[username][2].append(pl)
            global_ranking[pl][3] += 1


def assign_pref(pref_list):
    for pl, v in pref_list.items():
        if pl not in global_pref:
            global_pref[pl] = [0, 0]
        else:
            global_pref[pl][0] += v
            global_pref[pl][1] += 1


def save_pref(data):
    with open('output/preference.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'Preference'])
        for k, v in data.items():
            w.writerow([k, v])


def save_data(data, filename, column):
    with open(f'output/{filename}.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([column, 'WR', 'Total games'])
        for k, v in data.items():
            w.writerow([k, v['win'], v['total']])


def save_hours(data):
    with open(f'output/hours_wr.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player: WR (Total games)'] + hours_header)
        for k in data.keys():
            w.writerow([k] + [str(data[k][h]['win']) + f'% ({data[k][h]["total"]})' for h in hours_header])


def update_avg_pref():
    for k, v in global_pref.items():
        try:
            global_pref[k] = round(v[0] / v[1], 2)
        except ZeroDivisionError:
            global_pref[k] = -1


def update_wr(data, ind_key, ind_val):
    for k, v in data.items():
        try:
            data[k][ind_key] = round(v[ind_key] * 100 / v[ind_val], 2)
        except ZeroDivisionError:
            data[k][ind_key] = 0
    return data


def update_rank(data, ind_key, ind_val):
    for k, v in data.items():
        try:
            data[k][ind_key] = round(v[ind_key] / v[ind_val], 2)
        except ZeroDivisionError:
            data[k][ind_key] = 0
    return data


def update_hours(data, ind_key, ind_val):
    for k, v in data.items():
        for k1, v1 in v.items():
            try:
                data[k][k1][ind_key] = round(v1[ind_key] * 100 / v1[ind_val], 2)
            except ZeroDivisionError:
                data[k][k1][ind_key] = 0
    return data


def save_plots(data):
    for k, v in data.items():
        x = hours_header
        y = [v[key]['win'] for key in v.keys()]
        n = [v[key]['total'] for key in v.keys()]
        plt.figure(figsize=(12, 5))
        plt.xlabel('Hours (UTC)')
        plt.ylabel('Total games (#)')
        plt.scatter(x, n)
        for i, txt in enumerate(y):
            plt.annotate(txt, (x[i], n[i]))
        plt.title('Win/loss ratio (%)')
        plt.plot(x, n)
        plt.savefig(f'output/plots/totals_hours/{k}.png')


def global_sort(global_list, ind_col):
    return {k: v for k, v in sorted(global_list.items(), key=lambda item: (-item[1][ind_col]))}


def save_purples(data):
    with open(f'output/purples.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Players', '# with purples'])
        purples_list = purples.get_purples()
        for k, v in data.items():
            if k not in purples_list:
                w.writerow([k, v])


start = time.time()
print('Start time:', datetime.now())
with open('input/list_of_players.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

logging.basicConfig(filename='main.log', level=logging.DEBUG)
results = {}
results_bga = {}
global_ranking = {k: [0, [], [], 0] for k in users}
# preference - count
global_pref = {k: [0, 0] for k in users}
top = 5
rank_all_players = {k: [] for k in users}
global_teams = {}
global_hours = {}
hours_header = [ut.add_zero(i) for i in range(0, 24)]
global_purples = {}
for u in users:
    logging.debug(f'Current user: {u}')
    items = ut.open_stats(u)
    results[u] = c.get_all_stats(items, 'all')
    results_bga[u] = c.get_all_stats(items, 'bga')
    logging.debug('Stats are split by variant types.')
    # group by players
    players_list = pls.get_players_set(items, u)
    if u == 'Valetta6789':
        players_dict = wl.get_players_dict(items, players_list)
        wl.save_players_dict(u, players_dict)
    logging.debug('Stats filtered by players are calculated.')
    # get top 10
    list_for_tops = wl.get_overall_wr(items, players_list)
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
    logging.debug('Top/bottom 10 calculations are finished.')
    # preferences: {player: preference}
    pref = wl.get_preference(list_for_tops)
    assign_pref(pref)
    logging.debug('Preference is calculated.')
    # group by teams
    teams = wl.group_by_teams(items)
    global_teams = global_teams | teams
    logging.debug('Stats grouped by teams.')
    global_hours[u] = wl.get_hours(items)
    # global_purples[u] = purples.count_purples(u, items)
    logging.debug('Hours and purples are calculated.')

print('Data is generated.')

save_to_tsv('up_to_date_stats', results)
save_wr('all', results)
save_wr('bga', results_bga)
logging.debug('WRs are saved.')

global_ranking = update_rank(global_ranking, 0, 3)
save_ranking(global_sort(global_ranking, 0))
logging.debug('Ranking is saved.')

update_avg_pref()
global_pref = {k: v for k, v in sorted(global_pref.items(), key=lambda item: -item[1])}
save_pref(global_pref)
logging.debug('Preference is saved.')

global_teams = update_wr(global_teams, 'win', 'loss')
save_data(global_sort(global_teams, 'win'), 'teams_wr', 'Team')
logging.debug('Teams are saved.')

global_hours = update_hours(global_hours, 'win', 'loss')
save_hours(global_hours)
# save_plots(global_hours)
logging.debug('Hours and plots are saved.')

# global_purples = {k: v for k, v in sorted(global_purples.items(), key=lambda item: -item[1])}
# save_purples(global_purples)
# user = 'Valetta6789'
# val_items = ut.open_stats(user)
# purples.get_games(user, val_items)
# logging.debug('Purples are saved.')

print('End time:', datetime.now())
print('Time spent (in min):', round((time.time() - start) / 60, 2))

import csv
import itertools

import numpy as np
import pandas as pd
import py.calc as c


def get_players_list(username):
    with open(f'../temp/{username}_players.txt', 'r', encoding='utf-8') as f:
        return [line.rstrip() for line in f.readlines()]


def get_players_dict(username, players):
    results = {}
    for p in players:
        main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(username)
        main_stats, list_easy, list_null, list_sd, list_dd = \
            c.get_filtered_by_var_not(main_stats), \
            c.get_filtered_by_var_not(list_easy), \
            c.get_filtered_by_var_not(list_null), \
            c.get_filtered_by_var_not(list_sd), \
            c.get_filtered_by_var_not(list_dd)
        p_wins = c.get_wins(get_filtered_by_player(p, main_stats))
        p_losses = c.get_losses(get_filtered_by_player(p, main_stats))
        p_total = p_wins + p_losses
        if p_total < 20:
            continue
        p_ratio = c.p(p_wins, p_losses)
        # p_w_ratio = c.p(p_wins, p_total)
        # p_l_ratio = c.p(p_losses, p_total)
        easy_ratio, null_ratio, sd_ratio, dd_ratio =\
            c.p(len(get_filtered_by_player(p, list_easy)), p_total),\
            c.p(len(get_filtered_by_player(p, list_null)), p_total),\
            c.p(len(get_filtered_by_player(p, list_sd)), p_total),\
            c.p(len(get_filtered_by_player(p, list_dd)), p_total)
        results[p] = {'wl': p_ratio, 'total': p_total, 'easy': easy_ratio, 'null': null_ratio,
                      'sd': sd_ratio, 'dd': dd_ratio}
    return {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['wl'], reverse=True)}


def get_filtered_by_player(player, stats):
    return [row for row in stats if player in row.players]


def save_players_dict(username, data):
    with open(f'../output/filtered_by_players/{username}_wl_by_players.tsv', 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            'Player name', 'W/L(%)', 'Total games', 'Easy', 'Null', 'Single dark', 'Double dark']
        )
        for k, v in data.items():
            w.writerow([
                k,
                v['wl'],
                v['total'],
                v['easy'],
                v['null'],
                v['sd'],
                v['dd']
            ])


def get_overall_wr(username, players):
    results = {}
    stats_3 = filter_var(username)
    for p in players:
        p_wins = c.get_wins(get_filtered_by_player(p, stats_3))
        p_losses = c.get_losses(get_filtered_by_player(p, stats_3))
        p_total = p_wins + p_losses
        if p_total <= 100:
            continue
        p_ratio = c.p(p_wins, p_losses)
        results[p] = {'wl': p_ratio, 'total': p_total}
    return sort_by_wl_games(results)


def get_preference(players_by_wl):
    results = {}
    ld = len(players_by_wl)
    for p in players_by_wl.keys():
        results[p] = (ld - list(players_by_wl.keys()).index(p) - 1) / ld
    return results


def filter_var(username):
    main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(username)
    return list(itertools.chain.from_iterable([
        c.get_filtered_by_var_not(list_easy),
        c.get_filtered_by_var_not(list_null),
        c.get_filtered_by_var_not(list_sd)])
    )


def sort_by_wl_games(data):
    d = {k: v for k, v in sorted(data.items(), key=lambda item: item[1]['wl'], reverse=True)}
    return d


def get_top_n(n, data):
    data = sort_by_wl_games(data)
    di = min(len(data), n)
    return dict(list(data.items())[:di])


def get_bottom_n(n, data):
    data = sort_by_wl_games(data)
    di = min(len(data), n)
    return dict(list(data.items())[-di:])


def group_by_teams(username):
    main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(username)
    results = {}
    for row in c.get_filtered_by_var_not(main_stats):
        p = row.players
        if p not in results:
            results[p] = {'win': 0, 'loss': 0, 'total': 0}
        if row.score == row.max_score:
            results[p]['win'] += 1
        else:
            results[p]['loss'] += 1
        results[p]['total'] += 1
    return {k: v for k, v in results.items() if v['total'] >= 50}

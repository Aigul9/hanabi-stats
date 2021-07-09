import csv
import itertools
import py.calc as c
import py.utils as ut


def get_players_dict(items, players):
    results = {}
    for p in players:
        main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(items)
        p_wins = c.get_wins(ut.contains_user(p, main_stats))
        p_losses = c.get_losses(ut.contains_user(p, main_stats))
        p_total = p_wins + p_losses
        if p_total < 20:
            continue
        p_ratio = ut.p(p_wins, p_losses)
        easy_ratio, null_ratio, sd_ratio, dd_ratio =\
            ut.p(len(ut.contains_user(p, list_easy)), p_total),\
            ut.p(len(ut.contains_user(p, list_null)), p_total),\
            ut.p(len(ut.contains_user(p, list_sd)), p_total),\
            ut.p(len(ut.contains_user(p, list_dd)), p_total)
        results[p] = {'wl': p_ratio, 'total': p_total, 'easy': easy_ratio, 'null': null_ratio,
                      'sd': sd_ratio, 'dd': dd_ratio}
    return {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['wl'], reverse=True)}


def save_players_dict(username, data):
    with open(f'output/filtered_by_players/{username}_wl_by_players.tsv', 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            'Player', 'W/L(%)', 'Total games', 'Easy', 'Null', 'Single dark', 'Double dark']
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


def get_overall_wr(items, players):
    results = {}
    stats_3 = filter_var(items)
    # print(stats_3)
    for p in players:
        p_wins = c.get_wins(ut.contains_user(p, stats_3))
        p_losses = c.get_losses(ut.contains_user(p, stats_3))
        p_total = p_wins + p_losses
        if p_total <= 100:
            continue
        p_ratio = ut.p(p_wins, p_losses)
        results[p] = {'wl': p_ratio, 'total': p_total}
    return sort_by_wl_games(results)


def get_preference(players_by_wl):
    results = {}
    ld = len(players_by_wl)
    for p in players_by_wl.keys():
        results[p] = (ld - list(players_by_wl.keys()).index(p) - 1) / ld
    return results


def filter_var(items):
    main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(items)
    return list(itertools.chain.from_iterable([list_easy, list_null, list_sd]))


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


def group_by_teams(items):
    main_stats = items
    results = {}
    for row in main_stats:
        p = ', '.join(row['playerNames'])
        results = form_totals_dict(p, results, row)
    return {k: v for k, v in results.items() if v['total'] >= 50}


def get_hours(items):
    main_stats = items
    hours_header = [ut.add_zero(i) for i in range(0, 24)]
    hours = {key: {'win': 0, 'loss': 0, 'total': 0} for key in hours_header}
    for row in main_stats:
        hour = row['datetimeFinished'][11:13]
        hours = form_totals_dict(hour, hours, row)
    return hours


def form_totals_dict(item, totals_dict, row):
    if item not in totals_dict:
        totals_dict[item] = {'win': 0, 'loss': 0, 'total': 0}
    if row['score'] == ut.get_max_score(row['options']['variantName']):
        totals_dict[item]['win'] += 1
    else:
        totals_dict[item]['loss'] += 1
    totals_dict[item]['total'] += 1
    return totals_dict

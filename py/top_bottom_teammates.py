import csv
import math

import py.utils as u
from database.db_connect import session, Game, Player, Variant


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


def get_top_bottom_lists(list_for_tops, top):
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
    list_top_n = get_top_n(top, first_half)
    list_bottom_n = get_bottom_n(top, second_half)
    return [list_top_n, list_bottom_n]


def save_ranking(data, rank_all_players):
    with open('output/rank/rank_avg.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'Rank', 'Seek', 'Hide'])
        for k, v in u.sort(data, 0).items():
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
            w.writerow([
                k,
                v[0],
                ', '.join(list_top),
                ', '.join(list_bottom)
            ])


if __name__ == "__main__":
    users = session.query(Player.player).all()
    top = 5
    rank_all_players = {k: [] for k in users}
    global_ranking = {k: [0, [], [], 0] for k in users}
    for user in users:
        user = user[0]
        # Step 3: Ranking based on top and bottom 10 teammates
        list_for_tops = wl.get_overall_wr(user_stats, players_list)
        rank_all_players[user] = wl.get_top_bottom_lists(list_for_tops, top)
    # rank/rank_avg.tsv
    for k, v in global_ranking.items():
        global_ranking[k][0] = u.p1(v[0], v[3])
    u.save_ranking(global_ranking, rank_all_players)
import csv
import errno
import logging
import os
import requests
from datetime import datetime
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler('errors.log')
fileHandler.setLevel(logging.INFO)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)


# Parsing
def open_stats(user, session=None):
    url = f'https://hanab.live/history/{user}?api'
    if session is None:
        response = requests.get(url)
    else:
        response = session.get(url)
    return response.json()


def open_stats_by_game_id(response, game_id):
    return [s for s in response if s['id'] == game_id][0]


def export_game(game_id, session=None):
    url = f'https://hanab.live/export/{game_id}'
    if session is None:
        response = requests.get(url)
    else:
        response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Read-write
def open_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip() for line in f.readlines()]


def open_tsv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip().split('\t') for line in f.readlines()]


def open_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip().split(',') for line in f.readlines()]


def files_in_dir(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def save(path, data, header):
    with open(f'{path}.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(header)
        for k, v in data.items():
            w.writerow([k, *v])


def save_value(path, data):
    with open(f'{path}.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        for k, v in data.items():
            w.writerow([k, v])


def save_csv(path, data):
    with open(f'{path}.csv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        for v in data:
            w.writerow(*v)


def save_header(path, header):
    with open(f'{path}.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(header)


# HQL-related functions
def clear_2p(stats):
    return [row for row in stats if int(row['options']['numPlayers']) != 2]


def clear_speedruns(stats):
    return [row for row in stats if not row['options']['speedrun']]


def get_2p(stats):
    return [row for row in stats if int(row['options']['numPlayers']) == 2]


def get_3p(stats):
    return [row for row in stats if int(row['options']['numPlayers']) == 3]


def filter_bga(stats):
    return [row for row in stats if row['options']['variantName'] in ('Rainbow (6 Suits)', 'No Variant', '6 Suits')]


def filter_non_bga(stats):
    return [row for row in stats if row['options']['variantName'] not in ('Rainbow (6 Suits)', 'No Variant', '6 Suits')]


def contains_user(stats, user):
    return [row for row in stats if user in row['playerNames']]


def filter_by_id(stats, ids):
    if len(ids) == 2:
        return [row for row in stats if ids[0] <= row['id'] <= ids[1]]
    if len(ids) == 1:
        return [row for row in stats if row['id'] >= ids[0]]
    else:
        print('Not filtered by id.')
        return stats
    

def filter_id_notes(stats):
    return filter_by_id(stats, [103000])
    

def get_wins(stats):
    return len([row for row in stats if row['score'] == get_max_score(row['options']['variantName'])])


def get_losses(stats):
    return len([row for row in stats if row['score'] != get_max_score(row['options']['variantName'])])


def get_wins_db(stats):
    return len([row for row in stats if row.score == get_max_score(row.variant)])


def get_losses_db(stats):
    return len([row for row in stats if row.score != get_max_score(row.variant)])


# Specific functions
def get_number_of_suits(variant):
    default_suits = {
        '3 Suits': 3,
        '4 Suits': 4,
        'No Variant': 5,
        '6 Suits': 6,
        'Dual-Color Mix': 6,
        'Ambiguous Mix': 6,
        'Ambiguous & Dual-Color': 6
    }

    return int(default_suits.get(variant, variant[-8:-7]))


def get_max_score(variant):
    return get_number_of_suits(variant) * 5


def convert_action_types(action_type):
    action_types = ['play', 'discard', 'color', 'rank']
    return action_types[action_type]


def get_action_type_length(actions, action_type):
    return len([a for a in actions if a['type'] == action_type])


def get_player_index(game, player):
    return game['players'].index(player)


def get_card_index(game, card):
    return game['deck'].index(card)


def switch_rank_mod(indices, index):
    return indices[(index + 2) % len(indices)]


def switch_rank_mod_next(indices, index):
    return indices[(index + 1) % len(indices)]


def get_number_of_starting_cards(n_players, one_less_card, one_extra_card):
    return get_number_of_cards_in_hand(n_players, one_less_card, one_extra_card) * n_players


def get_number_of_cards_in_hand(n_players, one_less_card, one_extra_card):
    cards = {
        2: 5,
        3: 5,
        4: 4,
        5: 4,
        6: 3
    }
    if one_less_card:
        return cards[n_players] - 1
    if one_extra_card:
        return cards[n_players] + 1
    return cards[n_players]


def get_number_of_plays_or_discards(actions):
    return len([a for a in actions if a.action_type in [0, 1]])


def is_clued(action):
    return action.action_type in [2, 3]


def is_played(piles, card_suit_ind, card_rank):
    suit_stack, direction = piles[card_suit_ind]
    if direction == 'up':
        return suit_stack + 1 == card_rank
    elif direction == 'down':
        return suit_stack - 1 == card_rank
    elif direction == '':
        if suit_stack == 0 and card_rank in (1, 5, 7):
            return True
        if suit_stack == 7 and card_rank in [2, 4]:
            return True
        else:
            return False


def up_or_down_direction(piles, card_suit_ind, card_rank):
    direction = piles[card_suit_ind][1]
    if direction == '':
        directions = {
            1: 'up',
            2: 'up',
            4: 'down',
            5: 'down'
        }
        return directions.get(card_rank, '')
    return direction


# Additional functions
def p(value, total):
    if total != 0:
        return round(value * 100 / total, 2)
    else:
        return 0


def p1(value, total):
    if total != 0:
        return round(value / total, 2)
    else:
        return 0


def p_no_round(value, total):
    if total != 0:
        return round(value * 100 / total)
    else:
        return 0


def add_zero(hour):
    if hour < 10:
        return '0' + str(hour)
    else:
        return str(hour)


def r(num):
    return str(num).replace('.', ',')


def current_time():
    return datetime.now()


def time_spent(start_time):
    return current_time() - start_time


def convert_sec_to_day(n):
    n = int(n)
    day = n // (24 * 3600)
    n = n % (24 * 3600)
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n
    return {'days': day, 'hours': hour, 'minutes': minutes, 'seconds': seconds}


# Sort
def sort(data, col_ind):
    return {k: v for k, v in sorted(data.items(), key=lambda item: -item[1][col_ind])}


def sort_by_key(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: x[0].lower())}


def sort_by_value(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: (-x[1]))}


# Save
def save_up_to_date_stats(data):
    with open('output/up_to_date_stats.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            'Username', 'Type',
            'W/L(%)', 'W(%)', 'L(%)', 'W(#)', 'L(#)',
            'W/L(%, 2p)', 'W(%, 2p)', 'L(%, 2p)', 'W(#, 2p)', 'L(#, 2p)',
            'W/L(%, 3p)', 'W(%, 3p+)', 'L(%, 3p+)', 'W(#, 3p+)', 'L(#, 3p+)']
        )
        for k, v in sort_by_key(data).items():
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


def save_wr(data):
    with open('output/winrate/highest_wr.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'W(%)', 'Total games'])
        for k, v in sorted(data.items(), key=lambda item: item[1]['Totals']['total_p'], reverse=True):
            w.writerow([
                k,
                v['Totals']['total_p'][0],
                v['Totals']['total_c'][2]
            ])


def save_ranking(data, rank_all_players):
    with open('output/rank/rank_avg.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Username', 'Rank', 'Seek', 'Hide'])
        for k, v in sort(data, 0).items():
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


def save_data(data, filename, column):
    with open(f'output/winrate/{filename}.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([column, 'WR', 'Total games'])
        for k, v in data.items():
            w.writerow([k, v['win'], v['total']])


def save_hours(data, hours_header):
    with open(f'output/time/hours_wr.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player: WR (Total games)'] + hours_header)
        for k in data.keys():
            w.writerow([k] + [str(data[k][h]['win']) + f'% ({data[k][h]["total"]})' for h in hours_header])


def save_plots(data, hours_header):
    for k, v in data.items():
        x = hours_header
        y = [v[key]['win'] for key in v.keys()]
        n = [v[key]['total'] for key in v.keys()]
        fig = plt.figure(figsize=(12, 5))
        plt.xlabel('Hours (UTC)')
        plt.ylabel('Total games (#)')
        plt.scatter(x, n)
        for i, txt in enumerate(y):
            plt.annotate(txt, (x[i], n[i]))
        plt.title('Win/loss ratio (%)')
        plt.plot(x, n)
        plt.savefig(f'output/time/plots/{k}.png')
        plt.close(fig)

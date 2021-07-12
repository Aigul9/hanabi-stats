import csv
import errno
import os
import requests
import time
from datetime import datetime


# Parsing
def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


def export_game(game_id):
    url = f'https://hanab.live/export/{game_id}'
    response = requests.get(url)
    return response.json()


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


def save(filename, data, header):
    with open(f'../output/{filename}.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(header)
        for k, v in data.items():
            w.writerow([k, *v])


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
    return default_suits.get(variant, variant[-8:-7])


def get_max_score(variant):
    return int(get_number_of_suits(variant)) * 5


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


def get_number_of_starting_cards(n_players):
    return n_players * 5 if n_players == 3 else n_players * 4


def get_number_of_plays_or_discards(actions):
    return len([a for a in actions if a['type'] in [0, 1]])


# Additional functions
def sort(data, col_ind):
    return {k: v for k, v in sorted(data.items(), key=lambda item: -item[1][col_ind])}


def p(value, total):
    if total != 0:
        return round(value * 100 / total, 2)
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
    print(f'Time spent (in min): {round((time.time() - start_time) / 60, 2)}')


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

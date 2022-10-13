import csv
import errno
import logging
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy import text

from database.db_connect import db

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)
logger = logging.getLogger(__name__)

# fileHandler = logging.FileHandler('../database/errors.log')
# fileHandler.setLevel(logging.DEBUG)
# logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)


def open_stats(user, session=None):
    """Gets user's statistics from the history page API.

    Parameters
    ----------
    user : str
        Player name
    session : session
        Current session

    Returns history in json format
    """
    user = 'Mat%C3%ADas%20V5' if user == 'Matías_V5' else user
    url = f'https://hanab.live/api/v1/history-full/{user}'
    if session is None:
        response = requests.get(url)
    else:
        response = session.get(url)
    return response.json()


def open_stats_from_id_start(user, id_start, session=None):
    """Gets user's statistics from the history page API starting from the game id.

    Parameters
    ----------
    user : str
        Player name
    id_start : int
        Start game id
    session : session
        Current session

    Returns history in json format starting from the game id
    """
    user = 'Mat%C3%ADas%20V5' if user == 'Matías_V5' else user
    url = f'https://hanab.live/api/v1/history-full/{user}?start={id_start}'
    if session is None:
        response = requests.get(url)
    else:
        response = session.get(url)
    return response.json()


def open_stats_by_game_id(response, game_id):
    """Filters user's statistics by game id.

    Parameters
    ----------
    response : list
        User's history in json
    game_id : int
        Game id

    Returns
    -------
    list
        The game from user's history
    """
    return [s for s in response if s['id'] == game_id][0]


def export_game(game_id, session=None):
    """Gets a specific game from API.

    Parameters
    ----------
    game_id : int
        Game id
    session : session
        Current session

    Returns the game in json format
    """
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
    """Creates a directory by a specific path.

    Parameters
    ----------
    path : str
        Path to directory
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def open_file(filename):
    """Opens a file.

    Parameters
    ----------
    filename : str
        File name
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip() for line in f.readlines()]


def read_file(filename):
    """Simply reads a file.

    Parameters
    ----------
    filename : str
        File name
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def open_tsv(filename):
    """Opens a tsv file.

    Parameters
    ----------
    filename : str
        File name
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip().split('\t') for line in f.readlines()]


def open_csv(filename):
    """Opens a csv file.

    Parameters
    ----------
    filename : str
        File name
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip().split(',') for line in f.readlines()]


def files_in_dir(path):
    """Combines file names in the directory.

    Parameters
    ----------
    path : str
        Path to directory

    Returns
    -------
    list
        File names in the directory
    """
    return [f for f in listdir(path) if isfile(join(path, f))]


def save(path, data, header):
    """Saves data with header into a tsv file.

    Parameters
    ----------
    path : str
        Path to directory
    data : dict
        Saved data
    header : list
        File header
    """
    with open(f'{path}.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(header)
        for k, v in data.items():
            w.writerow([k, *v])


def save_value(path, data):
    """Saves data into a tsv file.

    Parameters
    ----------
    path : str
        Path to directory
    data : dict
        Saved data
    """
    with open(f'{path}.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        for k, v in data.items():
            w.writerow([k, v])


def save_csv(path, data):
    """Saves list into a csv file.

    Parameters
    ----------
    path : str
        Path to directory
    data : list
        Saved data
    """
    with open(f'{path}.csv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        for v in data:
            w.writerow(*v)


def save_list_tsv(path, data):
    """Saves list into a tsv file.

    Parameters
    ----------
    path : str
        Path to directory
    data : list
        Saved data
    """
    with open(f'{path}.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        for v in data:
            w.writerow(v)


def save_header(path, header):
    """Saves header into a tsv file.

    Parameters
    ----------
    path : str
        Path to directory
    header : list
        File header
    """
    with open(f'{path}.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(header)


def clear_2p(stats):
    """Removes 2-player games from the user's json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History without 2-player games
    """
    return [row for row in stats if int(row['options']['numPlayers']) != 2]


def clear_speedruns(stats):
    """Removes speedruns from the user's json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History without speedruns
    """
    return [row for row in stats if not row['options']['speedrun']]


def get_2p(stats):
    """Gets 2-player games from the user's json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History of 2-player games
    """
    return [row for row in stats if int(row['options']['numPlayers']) == 2]


def get_3p(stats):
    """Gets 3-player games from the user's json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History of 3-player games
    """
    return [row for row in stats if int(row['options']['numPlayers']) == 3]


def filter_bga(stats):
    """Gets the user's json statistics only containing variants played on BGA.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History with only BGA variants
    """
    return [row for row in stats if row['options']['variantName'] in ('Rainbow (6 Suits)', 'No Variant', '6 Suits')]


def filter_non_bga(stats):
    """Gets the user's json statistics without variants played on BGA.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History without BGA variants
    """
    return [row for row in stats if row['options']['variantName'] not in ('Rainbow (6 Suits)', 'No Variant', '6 Suits')]


def contains_user(stats, user):
    """Gets the json statistics containing a specific user.

    Parameters
    ----------
    stats : list
        User's games
    user : str
        Player name

    Returns
    -------
    list
        History containing the user
    """
    return [row for row in stats if user in row['playerNames']]


def get_wins(stats):
    """Counts number of games finished with a perfect score using json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    int
        Number of games with a perfect score
    """
    return len([row for row in stats if row['score'] == get_max_score(row['options']['variantName'])])


def get_losses(stats):
    """Counts number of games not finished with a perfect score using json statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    int
        Number of games without a perfect score
    """
    return len([row for row in stats if row['score'] != get_max_score(row['options']['variantName'])])


def get_wins_db(stats):
    """Counts number of games finished with a perfect score using database.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    int
        Number of games with a perfect score
    """
    return len([row for row in stats if row.score == get_max_score(row.variant)])


def get_losses_db(stats):
    """Counts number of games not finished with a perfect score using database.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    int
        Number of games without a perfect score
    """
    return len([row for row in stats if row.score != get_max_score(row.variant)])


def get_number_of_suits(variant):
    """Gets number of suits for the variant.

    Parameters
    ----------
    variant : str
        Variant

    Returns
    -------
    int
        Number of suits for the variant
    """
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
    """Calculates the max score for the variant.

    Parameters
    ----------
    variant : str
        Variant

    Returns
    -------
    int
        Max score for the variant
    """
    return get_number_of_suits(variant) * 5


def get_action_type_length(actions, action_type):
    """Counts number of actions representing a specific action type.

    Parameters
    ----------
    actions : list
        Game actions
    action_type : int
        Action type

    Returns
    -------
    int
        Number of game actions containing the action type
    """
    return len([a for a in actions if a['type'] == action_type])


def get_player_index(game, player):
    """Gets a player index in an array.

    Parameters
    ----------
    game : dict
        Game in json format
    player : str
        Player name

    Returns
    -------
    int
        The player index
    """
    return game['players'].index(player)


def get_card_index(game, card):
    """Gets a card index in a deck.

    Parameters
    ----------
    game : dict
        Game in json format
    card : dict
        Card

    Returns
    -------
    int
        The card index
    """
    return game['deck'].index(card)


def get_number_of_starting_cards(n_players, one_less_card, one_extra_card):
    """Gets a total number of cards in players' starting hands.

    Parameters
    ----------
    n_players : int
        Number of players
    one_less_card : bool
        A flag representing one less card option
    one_extra_card : bool
        A flag representing one extra card option

    Returns
    -------
    int
        Number of cards in starting hands
    """
    return get_number_of_cards_in_hand(n_players, one_less_card, one_extra_card) * n_players


def get_number_of_cards_in_hand(n_players, one_less_card, one_extra_card):
    """Gets a number of cards in player's starting hand.

    Parameters
    ----------
    n_players : int
        Number of players
    one_less_card : bool
        A flag representing one less card option
    one_extra_card : bool
        A flag representing one extra card option

    Returns
    -------
    int
        Number of cards in each starting hand
    """
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
    """Counts a number of plays or discard in a game.

    Parameters
    ----------
    actions : list
        Game actions

    Returns
    -------
    int
        Number of plays or discards
    """
    return len([a for a in actions if a.action_type in [0, 1]])


def is_clued(action):
    """Checks if action represents a clue.

    Parameters
    ----------
    action : GameAction
        A game action

    Returns
    -------
    bool
        A flag representing whether a clue was given or not
    """
    return action.action_type in [2, 3]


def is_played(piles, card_suit_ind, card_rank):
    """Checks if a card is played.

    Parameters
    ----------
    piles : list
        Current state of the piles
    card_suit_ind : int
        Card suit
    card_rank : int
        Card rank

    Returns
    -------
    bool
        A flag representing whether a card is played or not
    """
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
    """Gets a direction for the 'Up or Down' variant.

    Parameters
    ----------
    piles : list
        Current state of the piles
    card_suit_ind : int
        Card suit
    card_rank : int
        Card rank

    Returns
    -------
    direction : str
        The current direction for the 'Up or Down' variant
    """
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


def p(value, total):
    """Calculates a percentage rounded to 2 decimal places.

    Parameters
    ----------
    value : int
        Current value
    total : int
        Total value

    Returns
    -------
    float
        Percentage rounded to 2 decimal places
    """
    if total != 0:
        return round(value * 100 / total, 2)
    else:
        return 0


def p1(value, total):
    """Divides two numbers and rounds the result to 2 decimal places.

    Parameters
    ----------
    value : int
        Current value
    total : int
        Total value

    Returns
    -------
    float
        The result of division rounded to 2 decimal places
    """
    if total != 0:
        return round(value / total, 2)
    else:
        return 0


def p_no_round(value, total):
    """Calculates a percentage without rounding.

    Parameters
    ----------
    value : int
        Current value
    total : int
        Total value

    Returns
    -------
    int
        Percentage without rounding
    """
    if total != 0:
        return round(value * 100 / total)
    else:
        return 0


def add_zero(hour):
    """Adds zero in front of the 1-digit numbers.

    Parameters
    ----------
    hour : int
        An hour

    Returns
    -------
    str
        2-digit hour
    """
    if hour < 10:
        return '0' + str(hour)
    else:
        return str(hour)


def r(num):
    """Replaces dots with commas in a number.

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    str
        Number in a string format with replaced dots
    """
    return str(num).replace('.', ',')


def current_time():
    """Gets current time.

    Returns
    -------
    datetime
        Current date and time
    """
    return datetime.now()


def time_spent(start_time):
    """Gets difference between current time and given time.

    Parameters
    ----------
    start_time : datetime
        Start time

    Returns
    -------
    int
        Difference in millis between current time and start time
    """
    return current_time() - start_time


def convert_sec_to_day(n):
    """Converts seconds to days, hour, minutes, and seconds.

    Parameters
    ----------
    n : int
        Number of seconds

    Returns
    -------
    dict
        Number of seconds split by days, hours, minutes, and seconds
    """
    n = int(n)
    day = n // (24 * 3600)
    n = n % (24 * 3600)
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n
    return {'days': day, 'hours': hour, 'minutes': minutes, 'seconds': seconds}


def sort(data, col_ind):
    """Sorts a dictionary by column index in descending order.

    Parameters
    ----------
    data : dict
        Initial dictionary
    col_ind : int
        Column index

    Returns
    -------
    dict
        A dictionary sorted by column index in descending order
    """
    return {k: v for k, v in sorted(data.items(), key=lambda item: -item[1][col_ind])}


def sort_by_key(data):
    """Sorts a dictionary by key in ascending order.

    Parameters
    ----------
    data : dict
        Initial dictionary

    Returns
    -------
    dict
        A dictionary sorted by key in ascending order
    """
    return {k: v for k, v in sorted(data.items(), key=lambda x: x[0].lower())}


def sort_by_value(data):
    """Sorts a dictionary by value in descending order.

    Parameters
    ----------
    data : dict
        Initial dictionary

    Returns
    -------
    dict
        A dictionary sorted by value in descending order
    """
    return {k: v for k, v in sorted(data.items(), key=lambda x: -x[1])}


def run_query(sql):
    """Runs a sql query.

    Parameters
    ----------
    sql : str
        A text containing a sql query.
    Returns
    -------
    list
        A list with results
    """
    result = db.execute(sql)
    return [row for row in result]


def run_workflow(path, header):
    """Workflow running a sql query and saving the results into tsv file.

    Parameters
    ----------
    path : str
        Path to the file location
    header : list
        Column names
    """
    sql_file = read_file(f'../../database/sql/{path}.sql')
    sql = text(sql_file)
    result = run_query(sql)
    save_header(f'../../{path}', header)
    save_list_tsv(f'../../{path}', result)


def get_total_games():
    url = 'https://hanab.live/stats'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return int(re.findall(r'\d+', soup.find('li').text)[0])

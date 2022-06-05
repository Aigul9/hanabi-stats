"""
Description:
    A pivot table containing a percentage of similarities between two players' vocabularies.
    It is based on previously extracted player's notes and calculated as a number of shared words
    divided by a number of total words in a first player's vocabulary.
    Figures for the same pair of players may differ if they have unequal number of words.

Columns:
    - Player: player name

Dimensions:
    - percentage of similarity
"""

import csv

import py.utils as u
from database.db_connect import session, Player


def open_notes_stats(username):
    """Gets user's portrait from a tsv file and converts the data into dictionary.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    dict
        Number of notes containing a specific word or symbol
    """
    with open(f'../../output/notes/portraits/{username}_portrait.tsv', 'r', encoding='utf-8') as file:
        player_notes_list = []
        for line in file.readlines():
            player_notes_list.append(line.rstrip().split('\t'))
    for n in player_notes_list:
        try:
            return {n[0]: n[1] for n in player_notes_list[1:]}
        except IndexError:
            print(username, n)


def get_voc_comparison(player_word_count_dict):
    """Creates a pivot table from players' vocabularies.

    Parameters
    ----------
    player_word_count_dict : dict
        Number of notes by word for each player

    Returns
    -------
    player_word_count_pivot : dict
        Pivot table containing percentage of similarities between two vocabularies
    """
    player_word_count_pivot = {}
    for player, word_count_dict in player_word_count_dict.items():
        player_comparison_list = []
        for count in player_word_count_dict.values():
            player_comparison_list.append(f'{compare(word_count_dict, count)}')
        player_word_count_pivot[player] = player_comparison_list
    return player_word_count_pivot


def compare(word_count_dict1, word_count_dict2):
    """Calculates percentage of comparison between two players' vocabularies.

    Parameters
    ----------
    word_count_dict1 : dict
        Number of notes by word of the first player
    word_count_dict2 : dict
        Number of notes by word of the second player
    Returns
    -------
    int
        Percentage of similarities
    """
    words_count1 = len(word_count_dict1)
    common_words_count = len(word_count_dict1.keys() & word_count_dict2.keys())
    try:
        return round(common_words_count / words_count1 * 100)
    except ZeroDivisionError:
        return 0


def save(player_word_count_pivot):
    """Saves compared players' vocabularies into a tsv file.

    Parameters
    ----------
    player_word_count_pivot : dict
        Pivot table containing percentage of similarities between two vocabularies
    """
    with open(f'../../output/notes/vocabulary_intersection.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player', *player_word_count_pivot.keys()])
        for k, v in player_word_count_pivot.items():
            w.writerow([k, *v])


if __name__ == "__main__":
    users_portraits = {}
    users = session.query(Player.player).all()
    for user in users:
        user = user[0]
        users_portraits[user] = open_notes_stats(user)
    save(get_voc_comparison(u.sort_by_key(users_portraits)))

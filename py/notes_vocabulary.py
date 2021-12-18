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
    with open(f'../output/notes/portraits/{username}_portrait.tsv', 'r', encoding='utf-8') as file:
        user_notes_list = []
        for line in file.readlines():
            user_notes_list.append(line.rstrip().split('\t'))
    for n in user_notes_list:
        try:
            return {n[0]: n[1] for n in user_notes_list[1:]}
        except IndexError:
            print(username, n)


def get_voc_comparison(user_word_frequency_dict):
    """Creates a pivot table from users' vocabularies.

    Parameters
    ----------
    user_word_frequency_dict : dict
        Number of notes by word for each player

    Returns
    -------
    user_word_frequency_pivot : dict
        Pivot table containing percentage of similarities between two vocabularies
    """
    user_word_frequency_pivot = {}
    for player, word_frequency_dict in user_word_frequency_dict.items():
        player_comparison_list = []
        for frequency in user_word_frequency_dict.values():
            player_comparison_list.append(f'{compare(word_frequency_dict, frequency)}%')
        user_word_frequency_pivot[player] = player_comparison_list
    return user_word_frequency_pivot


def compare(word_frequency_dict1, word_frequency_dict2):
    """Calculates percentage of comparison between two users' vocabularies.

    Parameters
    ----------
    word_frequency_dict1 : dict
        Number of notes by word of the first player
    word_frequency_dict2 : dict
        Number of notes by word of the second player
    Returns
    -------
    int
        Percentage of similarities
    """
    words_count1 = len(word_frequency_dict1)
    common_words_count = len(word_frequency_dict1.keys() & word_frequency_dict2.keys())
    try:
        return round(common_words_count / words_count1 * 100)
    except ZeroDivisionError:
        return 0


def save(user_word_frequency_pivot):
    """Saves compared users' vocabularies into a tsv file.

    Parameters
    ----------
    user_word_frequency_pivot : dict
        Pivot table containing percentage of similarities between two vocabularies
    """
    with open(f'../output/notes/vocabulary_intersection.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player', *user_word_frequency_pivot.keys()])
        for k, v in user_word_frequency_pivot.items():
            w.writerow([k, *v])


if __name__ == "__main__":
    users_portraits = {}
    users = session.query(Player.player).all()
    for user in users:
        user = user[0]
        users_portraits[user] = open_notes_stats(user)
    save(get_voc_comparison(u.sort_by_key(users_portraits)))

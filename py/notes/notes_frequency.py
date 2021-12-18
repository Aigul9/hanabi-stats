import csv

from py.notes.notes_vocabulary import open_notes_stats
from database.db_connect import session, Player


def most_frequent(player_word_count_dict):
    """Gets number of the most frequent words from top players' vocabularies.

    Parameters
    ----------
    player_word_count_dict : dict
        Number of words grouped by a word and player

    Returns
    -------
    dict
        Number of words and list of players who have the same word in a vocabulary grouped by a word
    """
    word_count_players_dict = {}
    for player, word_frequency_dict in player_word_count_dict.items():
        for word, count in word_frequency_dict.items():
            if word in word_count_players_dict:
                word_count_players_dict[word][0] += int(count)
                word_count_players_dict[word][1].append(word)
            else:
                word_count_players_dict[word] = [int(count), [player]]
    return {k: v for k, v in sorted(word_count_players_dict.items(), key=lambda x: (-x[1][0]))}


def save_words(word_count_players_dict, users_count):
    """Saves frequency of words and number of common vocabularies grouped by a word into a tsv file.

    Parameters
    ----------
    word_count_players_dict : dict
        Frequency of words and number of common vocabularies grouped by a word
    users_count : int
        Number of players
    """
    with open(f'../../output/notes/frequent_words.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Words', 'Frequency', f'Number of vocabularies (Max = {users_count})'])
        for word, count_players_list in word_count_players_dict.items():
            if count_players_list[0] >= 100:
                v_len = len(count_players_list[1])
                r = str(v_len)
                w.writerow([word, count_players_list[0], r])


if __name__ == "__main__":
    users_portraits = {}
    users = session.query(Player.player).all()
    for user in users:
        user = user[0]
        users_portraits[user] = open_notes_stats(user)
    save_words(most_frequent(users_portraits), len(users))

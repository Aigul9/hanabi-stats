import csv
import re

from database.db_connect import session, Player, PlayerNotes


def decode(note):
    """Replaces character reference with an actual character.

    Parameters
    ----------
    note : str
        Player's note

    Returns
    -------
    note : str
        Player's note with replaced symbols
    """
    html_codes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('"', '&#34;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in html_codes:
        note = note.replace(code[1], code[0])
    return note


def save(username, word_frequency_dict):
    """Saves user's notes portrait into a tsv file.

    Parameters
    ----------
    username : str
        Player name
    word_frequency_dict : dict
        Number of notes containing a specific word or symbol
    """
    with open(f'../../output/notes/portraits/{username}_portrait.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Note', f'Frequency ({sum([v for v in word_frequency_dict.values()])} in total)'])
        for k, v in word_frequency_dict.items():
            w.writerow([k, v])


def update_user_notes(notes, word_frequency_dict):
    """Decodes user's notes, splits by punctuation symbols, extracts only words from a note.

    Parameters
    ----------
    notes : list
        Player's note for a particular game
    word_frequency_dict : dict
        Number of notes containing a specific word or symbol
    Returns
    -------
    word_frequency_dict : dict
        Updated dictionary of notes with added notes for the next game
    """
    notes = [decode(n) for n in notes if n != '']
    for n in notes:
        n_arr = re.split(r'[ |,]+', n)
        for n1 in n_arr:
            ex_punctuation = ['-', '=', '/', '', ' ']
            if n1 in ex_punctuation:
                continue
            r = re.compile(r"(\w+)[,.?!]+$")
            m = r.match(n1)
            if m is not None:
                n1 = r.findall(n1)[0]
            n1 = n1.lower()
            n1 = n1.replace('"', '')
            if n1 in word_frequency_dict:
                word_frequency_dict[n1] += 1
            else:
                word_frequency_dict[n1] = 1
    return word_frequency_dict


def get_notes_stats(username):
    """Calculated frequency of words for a specified player.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    word_frequency_dict : dict
        Number of notes containing a specific word or symbol
    """
    word_frequency_dict = {}
    notes_list = session.query(PlayerNotes.notes)\
        .filter(PlayerNotes.player == username)\
        .all()
    for notes in notes_list:
        word_frequency_dict = update_user_notes(notes[0], word_frequency_dict)
    return word_frequency_dict


if __name__ == "__main__":
    users = session.query(Player.player).all()
    for user in users:
        user = user[0]
        user_portrait = get_notes_stats(user)
        user_portrait = {k: v for k, v in sorted(user_portrait.items(), key=lambda x: (-x[1], x[0]))}
        save(user, user_portrait)

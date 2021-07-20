import csv
import re

from database.db_connect import session, PlayerNotes
import py.utils as u


def decode(note):
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


def save(username, data):
    with open(f'output/notes/portraits/{username}_portrait.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Note', f'Frequency ({sum([v for v in data.values()])} in total)'])
        for k, v in data.items():
            w.writerow([k, v])


def save_count(user, data_user):
    with open('output/notes/notes_count.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
        w.writerow([user, data_user['count'], data_user['len']])


def update_notes_count(notes, notes_count):
    # notes per game
    n_len = len([r for r in notes if r != ''])
    notes_count['len'] += n_len
    notes_count['count'] += 1
    return notes_count


def update_user_notes(notes, user_portrait):
    # portrait
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
            if n1 in user_portrait:
                user_portrait[n1] += 1
            else:
                user_portrait[n1] = 1
    return user_portrait


def get_notes_stats(user, stats):
    stats = u.filter_id_notes(stats)
    user_portrait = {}
    notes_count = {
        'len': 0,
        'count': 0
    }
    for s in stats:
        g_id = s['id']
        notes = session.query(PlayerNotes.notes)\
            .filter(PlayerNotes.game_id == g_id)\
            .filter(PlayerNotes.player == user)\
            .scalar()
        if notes is not None:
            user_portrait = update_user_notes(notes, user_portrait)
            notes_count = update_notes_count(notes, notes_count)
    notes_count['count'] = round(notes_count['len'] / notes_count['count'])
    return user_portrait, notes_count

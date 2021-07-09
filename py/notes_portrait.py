import csv
import re
import time
from datetime import datetime
import py.utils as ut


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


def filter_id_range(array):
    # 169428 - starting id for notes (17.05.2020)
    # 580462 - for testing purposes
    return [row for row in array if row['id'] >= 169428 and not row['options']['speedrun']]


def save(username, data):
    with open(f'../output/portraits/{username}_portrait.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Note', f'Frequency ({sum([v for v in data.values()])} in total)'])
        for k, v in data.items():
            w.writerow([k, v])


def save_count(user, data_user):
    with open(f'../output/notes_count_sorted.tsv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
        # w.writerow(['Note', 'Count', 'Per game'])
        w.writerow([user, data_user['len'], round(data_user['len'] / data_user['count'])])


with open('../input/list_of_players_notes.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


notes_count = {}
for u in users:
    print(u)
    start = time.time()
    ut.current_time()
    stats = filter_id_range(ut.open_stats(u))
    u_notes_dict = {}
    for s in stats:
        game = ut.export_game(s)
        try:
            notes = game['notes']
            pl_notes = notes[game['players'].index(u)]
            n_len = len([r for r in pl_notes if r != ''])
            if u in notes_count:
                notes_count[u]['len'] += n_len
                notes_count[u]['count'] += 1
            else:
                notes_count[u] = {}
                notes_count[u]['len'] = n_len
                notes_count[u]['count'] = 1
            # print(notes_count)
            # ex_notes = ['[f]', '[cm]', '', 'f', 'cm']
            # pl_notes = [decode(n) for n in pl_notes if n != '']
            # if len(pl_notes) == 0:
            #     continue
            # for n in pl_notes:
            #     n_arr = re.split(r'[ |,]+', n)
            #     for n1 in n_arr:
            #         ex_punctuation = ['-', '=', '/', '', ' ']
            #         if n1 in ex_punctuation:
            #             continue
            #         r = re.compile(r"(\w+)[,.?!]+$")
            #         m = r.match(n1)
            #         if m is not None:
            #             n1 = r.findall(n1)[0]
            #         n1 = n1.lower()
            #         # if n1 in u_notes_dict:
            #         #     u_notes_dict[n1] += 1
            #         # else:
            #         #     u_notes_dict[n1] = 1
        except KeyError:
            # print('pass', game['id'])
            pass
    # u_notes_dict = {k: v for k, v in sorted(u_notes_dict.items(), key=lambda x: (-x[1], x[0]))}
# save(u, u_notes_dict)
    save_count(u, notes_count[u])
    print(f'{u} is saved.')
    print('End time:', datetime.now())
    print('Time spent (in min):', round((time.time() - start) / 60, 2))

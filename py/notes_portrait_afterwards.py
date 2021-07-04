import csv
# import py.notes_portrait as np
import py.parsing as prs


def open_notes_stats(username):
    with open(f'../output/portraits/{username}_portrait.tsv', 'r', encoding='utf-8') as file:
        user_notes = []
        for line in file.readlines():
            user_notes.append(line.rstrip().split('\t'))
    for n in user_notes:
        try:
            return {n[0]: n[1] for n in user_notes[1:]}
        except IndexError:
            print(username, n)


def filter_id_range(array):
    # 169428 - starting id for notes (17.05.2020)
    return [row for row in array if row['id'] >= 169428 and not row['options']['speedrun']]


def most_talkative(data):
    talk = {}
    for k, v in data.items():
        stats = filter_id_range(prs.open_stats(k))
        talk[k] = round(sum([int(r) for r in v.values()]) / len(stats) * 100)
    return {k: v for k, v in sorted(talk.items(), key=lambda x: (-x[1]))}


def most_frequent(data):
    words = {}
    for k, v in data.items():
        for kw, vw in v.items():
            if kw in words:
                words[kw][0] += int(vw)
                words[kw][1].append(k)
            else:
                words[kw] = [int(vw), [k]]
    return {k: v for k, v in sorted(words.items(), key=lambda x: (-x[1][0]))}


def compare(stats1, stats2):
    num1 = len(stats1)
    inter = len(stats1.keys() & stats2.keys())
    return round(inter / num1 * 100)


def freq_names(data):
    global users
    aliases = {
        'asaelr': ['asa', 'asael', 'asaelr\'s', 'asa\'s'],
        'Dr_Kakashi': ['kakashi', 'kakash', 'kakashi:', 'kakashi\'s', 'kakashi\'-', '(kakashi'],
        'Fireheart': ['fire', 'fireheart\'s', 'fire\'s'],
        'Floriman': ['flo', 'flor', 'flori', 'florian', 'flor\'s', 'flori\'s', 'florian\'s?', 'floriman\'s'],
        'florrat2': ['florrat\'ll', 'florrat\'s', 'florrats'],
        'IAMJEFF': ['jeff'],
        'indego': ['inde', 'ind', 'indeog', 'indegos', 'indegoooooooo', 'indegoooo', 'indego?)', 'indego:',
                   'indego\'s?', 'indego\'s', 'indego\'d', 'inde:', 'inde\'s', 'ind'],
        'kimbifille': ['kimbi', 'kimb', 'kim', 'kim\'s', 'kimbo', 'kimbis', 'kimbi?)', 'kimbi)', 'kimbi\'s',
                       'kimbi\'s?', 'kim+timo', 'kimbi/piano', '(kimbi'],
        'Lanvin': ['lan', 'lanvi', 'lanvins', 'lanvinv', 'lanvvin', 'lanin', 'lanvin/sucu', 'lenvin', 'jack/lanvin',
                   'lanvin\'d', 'lanvin\'s', 'lanvin\'s?', 'lanvins', 'rah/lanvin', '(lanvin'],
        'Lel0uch': ['lel', 'lels', 'lelouch', 'lelll', 'lellll', 'sin/lel', 'lel:', 'lel\'s', 'g4/lel'],
        'Libster': ['lib', 'lib&i', 'lib\'s', 'libs', 'lib+mercy', 'libster\'s', 'libsters', '(libster'],
        'MarkusKahlsen': ['markus', 'markus:', 'markus\'s', 'markus\'', 'marku\'s', 'marku'],
        'melwen': ['mel', '(mel', 'mel\'s', 'mel:', 'mel?)', 'melwen\'s', 'melwen)', 'melwen:', 'melwens'],
        'Nitrate': ['nitrate', 'nitrate\'s', 'nitrates'],
        'Nitrate2': ['nitrate', 'nitrate\'s', 'nitrates', 'nitrate2'],
        'NoMercy': ['mercy', 'nomercy)', 'nomercy\'s', 'mercy\'s', 'lib+mercy'],
        'pianoblook': ['piano', '(piano', '(future-pianoblook:', 'kimbi/piano', 'piano\'s', 'piano?)',
                       'pianoblook', 'pianoblook\'s', 'pianos'],
        'RaKXeR': ['rak', 'rakxer\'s'],
        'scharkbite': ['schark', 'shark', 'schark\'s', 'schark)', 'scharkbite\'s', 'scharkie', 'scharks', '(schark'],
        'sephiroth': ['seph', 'seph\'d', 'seph\'s', 'seph\'s?', 'seph:', 'sephi', 'sephi\'s', 'sephiroth\'s',
                      'sephiroth/', 'septh'],
        'sin_faith': ['sin', 'sin\'s', 'sin/lel', 'sin:', 'sin_forget_y5', 'sin_mistake', 'sin_troll', 'sin_troll\'s',
                      'sin_troll)', 'sin_troll:', 'sin_trolled', '(sin', '!sin'],
        'sjdrodge': ['stephen', '(stephen', 'stephen\'s'],
        'Sucubis': ['suc', 'sucu', 'sucu\'s',  'sucu/time', 'lanvin/sucu'],
        'swineherd': ['swine', 'swine\'s', 'swine)', 'swineherd\'s', 'swinerherd'],
        'TimeHoodie': ['time\'s', 'hoodie', 'witt/time', 'timehoodie', 'timehoodie\'s', 'sucu/time'],
        'timotree': ['timo', 'timotree\'s', 'timotrees', 'kim+timo'],
        'Valetta6789': ['val', 'valetta\'s', 'valetta'],
        'VerySloppyTwo': ['sloppy', 'slop', 'slopp', 'verysloppy', 'slooopyyy', 'sloppy\'s', 'sloppy)', 'sloppys',
                          'slops'],
        'Zamiel': ['zam', 'zami'],
    }
    results = {}
    for k, v in data.items():
        users_lower = [u1.lower() for u1 in users]
        if k in users_lower:
            u_ind = users_lower.index(k)
            u_upper = users[u_ind]
            if u_upper in results:
                results[u_upper] += v[0]
            else:
                results[u_upper] = v[0]
                continue
        for a, av in aliases.items():
            if k in av:
                if a in results:
                    results[a] += v[0]
                else:
                    results[a] = v[0]
    return {k: v for k, v in sorted(results.items(), key=lambda x: (-x[1]))}


def save(data):
    with open(f'../output/vocabulary_intersection.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player', *data.keys()])
        for k, v in data.items():
            w.writerow([k, *v])


def save_words(words):
    with open(f'../output/frequent_words.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Words', 'Frequency', f'Number of vocabularies (All = {len(users)})'])
        for k, v in words.items():
            if v[0] >= 100:
                v_len = len(v[1])
                if v_len == len(users):
                    r = 'All'
                elif v_len > 5:
                    r = str(v_len)
                else:
                    r = f"{v_len}: {', '.join(v[1])}"
                w.writerow([k, v[0], r])


def save_dict(data):
    with open(f'../output/hanabi_dictionary.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Word', 'Frequency'])
        for k, v in sorted(data.items()):
            w.writerow([k, v[0]])


with open('../input/list_of_players_test.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

notes_stats = {}
for u in users:
    notes_stats[u] = open_notes_stats(u)

all_p = {}
for k1, v1 in notes_stats.items():
    k1_p = []
    for k2, v2 in notes_stats.items():
        k1_p.append(f'{compare(v1, v2)}%')
    all_p[k1] = k1_p

save(all_p)
#
# for p1, p2 in most_talkative(notes_stats).items():
#     print(f'{p1}\t{p2}')
#
save_words(most_frequent(notes_stats))

for n1, n2 in freq_names(most_frequent(notes_stats)).items():
    print(f'{n1}\t{n2}')

save_dict(most_frequent(notes_stats))

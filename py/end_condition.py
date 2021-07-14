import csv

import py.utils as ut


def sort_terminated(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: -x[1][4])}


def sort_strikeout(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: -x[1][2])}


def get_rate(num1, num2):
    return round(num1 / num2 * 100, 2)


def save(data):
    with open('../output/end_condition.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t')
        w.writerow([
            'Player',
            # 4
            'Terminated',
            # 2
            'Strikeout',
            # 3
            'Timeout',
            # 1
            'Normal'
        ])
        for k, v in data.items():
            t = v['total']
            w.writerow([
                k,
                get_rate(v[4], t),
                get_rate(v[2], t),
                get_rate(v[3], t),
                get_rate(v[1], t)
            ])


with open('../input/list_of_players_notes.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


global_term = {}
for u in users:
    print(u)
    stats = ut.clear_speedruns(ut.open_stats(u))
    local_term = {i: 0 for i in range(10)}
    for g in stats:
        e = g['endCondition']
        local_term[e] += 1
    local_term['total'] = len(stats)
    global_term[u] = local_term
save(global_term)

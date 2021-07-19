import csv

import py.utils as u


def sort_terminated(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: -x[1][4])}


def sort_strikeout(data):
    return {k: v for k, v in sorted(data.items(), key=lambda x: -x[1][2])}


def save(data):
    with open('output/end_condition.tsv', 'w', encoding='utf-8', newline='') as file:
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
                u.p(v[4], t),
                u.p(v[2], t),
                u.p(v[3], t),
                u.p(v[1], t)
            ])


def count_conditions(stats):
    conditions = {i: 0 for i in range(10)}
    for g in stats:
        ec = g['endCondition']
        conditions[ec] += 1
    conditions['total'] = len(stats)
    return conditions

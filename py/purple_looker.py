import requests
import csv
import calendar
from itertools import groupby


def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


def clear_2p(stats):
    return [row for row in stats if int(row['options']['numPlayers']) != 2]


def clear_speedruns(stats):
    return [row for row in stats if not row['options']['speedrun']]


def group_stats(stats):
    groups = groupby(stats, lambda row: row['datetimeFinished'][:7])
    grouped_stats = {}
    for k, v in groups:
        group = list(v)
        grouped_stats[k] = len(group)
    return {k: v for k, v in sorted(grouped_stats.items())}


def save(grouped_stats, user):
    with open(f'../output/purples/{user}.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['month', 'year', 'games'])
        for k, v in grouped_stats.items():
            month = calendar.month_abbr[int(k[5:])]
            year = k[:4]
            w.writerow([month, year, f'{v} games'])
        w.writerow([f'Total: {sum(grouped_stats.values())}', '', ''])


username = 'TimeHoodie'
data = group_stats(clear_2p(clear_speedruns(open_stats(username))))
save(data, username)

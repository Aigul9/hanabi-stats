import csv
from datetime import datetime
from itertools import groupby


def save(data):
    with open(f'output/time/times_spent.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player', 'Days', 'Hours', 'Per game (in min)', 'Per day (in h, incl. 0)', 'Per day (in h, excl. 0)'])
        for k, v in data.items():
            w.writerow([k, v[0]['days'], v[0]['hours'], v[1], v[2], v[3]])


def group_stats(data):
    groups = groupby(data, lambda row: row['datetimeFinished'][:10])
    keys = []
    for k, v in groups:
        keys.append(k)
    return len(keys)


# {'Valetta6789': [time, num_games, num_days_since_joined]}
# time in sec
# time / num_games (in min)
# time / num_days_since_joined (in h)


def get_times(stats):
    days_2 = group_stats(stats)
    date = stats[len(stats) - 1]['datetimeStarted']
    try:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    days_1 = (datetime.now() - d_joined).days
    times = [0, len(stats), days_1, days_2]
    for s in stats:
        try:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%SZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%SZ')
        diff = d_finish - d_start
        times[0] += diff.total_seconds()
    # per game
    times[1] = times[0] / times[1] / 60
    # per day
    times[2] = times[0] / times[2] / 3600
    # per day excl. days with 0 games
    times[3] = times[0] / times[3] / 3600
    return times

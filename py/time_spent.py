from datetime import datetime
import csv
import py.utils as ut


def save(data):
    with open(f'../output/times_spent.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player', 'Days', 'Hours', 'Per game (in min)', 'Per day (in h)'])
        for k, v in data.items():
            w.writerow([k, v[0]['days'], v[0]['hours'], v[1], v[2]])


users = ut.open_file('../input/list_of_players_notes.txt')
times = {}
# {'Valetta6789': [time, num_games, num_days_since_joined]}
# time in sec
# time / num_games (in min)
# time / num_days_since_joined (in h)
for u in users:
    stats = ut.clear_speedruns(ut.open_stats(u))
    date = stats[len(stats) - 1]['datetimeStarted']
    try:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    times[u] = [0, len(stats), (datetime.now() - d_joined).days]
    for s in stats:
        try:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%SZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%SZ')
        diff = d_finish - d_start
        times[u][0] += diff.total_seconds()
    # per game
    times[u][1] = times[u][0] / times[u][1] / 60
    # per day
    times[u][2] = times[u][0] / times[u][2] / 3600
times = {k: [ut.convert_sec_to_day(v[0]), round(v[1], 2), round(v[2], 2)] for k, v in sorted(times.items(), key=lambda i: -i[1][0])}
save(times)

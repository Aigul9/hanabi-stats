from datetime import datetime
import csv
import py.utils as ut


def save(data):
    with open(f'../output/times_spent.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player', 'Days', 'Hours', 'Minutes'])
        for k, v in data.items():
            w.writerow([k, v['days'], v['hours'], v['minutes']])


users = ut.open_file('../input/list_of_players_notes.txt')
times = {k: 0 for k in users}
for u in users:
    stats = ut.filter_non_bga(ut.clear_speedruns(ut.open_stats(u)))
    # stats = ut.clear_speedruns(ut.open_stats(u))
    for s in stats:
        try:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%SZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%SZ')
        diff = d_finish - d_start
        times[u] += diff.total_seconds()
times = {k: ut.convert_sec_to_day(v) for k, v in sorted(times.items(), key=lambda i: -i[1])}
save(times)

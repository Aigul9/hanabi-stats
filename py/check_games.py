import json


def open_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [json.loads(line.rstrip().replace('\'', '"')) for line in f.readlines()]


games = open_file('../temp/exported_games.txt')
n = 2906
for g, v in zip(games, range(n, 583000)):
    g_id = g['id']
    if int(g_id) != v:
        print(g_id, v)
        v = g_id
    v += 1

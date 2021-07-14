import csv
from datetime import datetime

import py.calc as c


def get_purples():
    with open('input/purples.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def get_purples_2():
    with open('input/purples_2.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def get_games(username, items):
    res = filter_purple_games(username, items)
    with open(f'output/misc/{username}_purple_games.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['game_id', 'count', 'score', 'variant', 'date', 'players'])
        for i in res:
            w.writerow([
                i['id'],
                i['options']['numPlayers'],
                i['score'],
                i['options']['variantName'],
                i['datetimeFinished'],
                i['playerNames']
            ])


def filter_purple_games(username, items):
    main_stats = c.get_list_3p(items)
    purples = get_purples()
    purples_2 = get_purples_2()
    games = []
    for game in main_stats:
        d_start = datetime(2020, 6, 1)
        d_game = datetime.strptime(game['datetimeFinished'][:10], '%Y-%m-%d')
        if username not in purples:
            if any(p in game['playerNames'] for p in purples)\
                    or (any(p in game['playerNames'] for p in purples_2) and d_game > d_start
                        and username not in purples_2):
                games.append(game)
    return games


def count_purples(username, items):
    games = filter_purple_games(username, items)
    return len(games)


def get_teachers(username, items):
    stats = items
    d_end = datetime(2019, 10, 20)
    teachers = {}
    for game in stats:
        d_game = datetime.strptime(game['datetimeFinished'][:10], '%Y-%m-%d')
        if d_game < d_end:
            t_list = game['playerNames']
            t_list.remove(username)
            for t in t_list:
                if t in teachers:
                    teachers[t] += 1
                else:
                    teachers[t] = 0
    teachers = dict(sorted(teachers.items(), key=lambda item: -item[1]))
    print(teachers)

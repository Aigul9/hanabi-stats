import py.calc as c
import csv
from datetime import datetime


def get_purples():
    with open('input/purples.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def get_purples_2():
    with open('input/purples_2.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def get_games(username):
    res = filter_purple_games(username)
    with open(f'output/{username}_purple_games.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['game_id', 'count', 'score', 'variant', 'date', 'players'])
        for i in res:
            w.writerow([i.game_id, i.count, i.score, i.variant, i.date, i.players])


def filter_purple_games(username):
    main_stats = c.get_list_3p(c.open_stats(username))
    purples = get_purples()
    purples_2 = get_purples_2()
    games = []
    for game in main_stats:
        d_start = datetime(2020, 6, 1)
        d_game = datetime.strptime(game.date[:10], '%Y-%m-%d')
        if username not in purples:
            if any(p in game.players for p in purples)\
                    or (any(p in game.players for p in purples_2) and d_game > d_start
                        and username not in purples_2):
                games.append(game)
    return games


def count_purples(username):
    games = filter_purple_games(username)
    return len(games)

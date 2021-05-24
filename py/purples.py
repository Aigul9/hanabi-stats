import py.calc as c
from datetime import datetime


def get_purples():
    with open('input/purples.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def get_purples_2():
    with open('input/purples_2.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def count_purples(username):
    k = 0
    main_stats = c.get_list_3p(c.open_stats(username))
    purples = get_purples()
    purples_2 = get_purples_2()
    for game in main_stats:
        d_start = datetime(2020, 6, 1)
        # print(game.date[:10])
        d_game = datetime.strptime(game.date[:10], '%Y-%m-%d')
        if username not in purples:
            if any(p in game.players for p in purples):
                k += 1
            if any(p in game.players for p in purples_2) and d_game > d_start\
                    and username not in purples_2:
                k += 1
    return k

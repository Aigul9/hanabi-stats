import py.calc as c


with open('input/purples.txt') as f:
    purples = [line.rstrip() for line in f.readlines()]


def count_purples(username):
    k = 0
    main_stats = c.open_stats(username)
    for game in main_stats:
        if any(p in game.players for p in purples) and username not in purples:
            k += 1
    return k

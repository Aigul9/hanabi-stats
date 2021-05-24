import py.calc as c


def get_purples():
    with open('input/purples.txt') as f:
        return [line.rstrip() for line in f.readlines()]


def count_purples(username):
    k = 0
    main_stats = c.open_stats(username)
    purples = get_purples()
    for game in main_stats:
        if any(p in game.players for p in purples) and username not in purples:
            k += 1
    return k

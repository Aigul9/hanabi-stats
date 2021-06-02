import py.calc as c


def get_max_scores(username):
    all_vars = {}
    stats = c.open_stats(username)
    stats.sort(key=lambda x: x.game_id)
    for game in stats:
        v = game.variant
        if v not in all_vars:
            all_vars[v] = 0
        all_vars[game.variant] = max(all_vars[game.variant], int(game.score))
    # print(all_vars)
    print(len(all_vars))


def get_gotten_vars(username):
    all_vars = {}
    stats = c.open_stats(username)
    stats.sort(key=lambda x: x.game_id)
    for game in stats:
        v = game.variant
        k = game.count
        if v not in all_vars:
            all_vars[v] = {'2': 'n', '3': 'n', '4': 'n', '5': 'n', '6': 'n'}
            if game.score == game.max_score:
                all_vars[v][k] = 'y'
            else:
                all_vars[v][k] = 'n'
    count = 0
    for k, v in sorted(all_vars.items()):
        for i in v:
            # print(k, v, i)
            if v[i] == 'y':
                count += 1
                print(k, end='\n')
    print(count)

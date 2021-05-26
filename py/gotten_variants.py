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
        if v not in all_vars:
            if game.score == game.max_score:
                all_vars[v] = 'gotten'
            else:
                all_vars[v] = 'not gotten'
    for k, v in sorted(all_vars.items()):
        if v == 'gotten':
            print(k, end='\n')
    print(len([all_vars for i in all_vars if all_vars[i] == 'gotten']))

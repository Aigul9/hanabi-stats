import py.calc as c


def get_max_scores(items):
    all_vars = {}
    stats = items
    stats.sort(key=lambda x: x['id'])
    for game in stats:
        v = game['options']['variantName']
        if v not in all_vars:
            all_vars[v] = 0
        all_vars[game['options']['variantName']] = max(all_vars[game['options']['variantName']], int(game['score']))
    print(len(all_vars))


def get_gotten_vars(items):
    all_vars = {}
    stats = items
    stats.sort(key=lambda x: x['id'])
    for game in stats:
        v = game['options']['variantName']
        k = game['options']['numPlayers']
        if v not in all_vars:
            all_vars[v] = {'2': 'n', '3': 'n', '4': 'n', '5': 'n', '6': 'n'}
            if game['score'] == c.get_max_score(v):
                all_vars[v][k] = 'y'
            else:
                all_vars[v][k] = 'n'
    count = 0
    for k, v in sorted(all_vars.items()):
        for i in v:
            if v[i] == 'y':
                count += 1
                print(k, end='\n')
    print(count)

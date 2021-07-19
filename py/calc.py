import py.utils as u


def get_totals(stat_list):
    results = {}
    # total - count
    total = len(stat_list)
    total_wins = u.get_wins(stat_list)
    total_losses = u.get_losses(stat_list)
    results['total_c'] = [total_wins, total_losses, total]
    # total - %
    results['total_p'] = [u.p(total_wins, total), u.p(total_losses, total), u.p(total_wins, total_losses)]
    # 2p - count
    list_2p = u.get_2p(stat_list)
    total = len(list_2p)
    total_wins = u.get_wins(list_2p)
    total_losses = u.get_losses(list_2p)
    results['total_2p_c'] = [total_wins, total_losses, total]
    # 2p - %
    results['total_2p_p'] = [u.p(total_wins, total), u.p(total_losses, total), u.p(total_wins, total_losses)]
    # 3p - count
    list_3p = u.clear_2p(stat_list)
    total = len(list_3p)
    total_wins = u.get_wins(list_3p)
    total_losses = u.get_losses(list_3p)
    results['total_3p_c'] = [total_wins, total_losses, total]
    # 3p - %
    results['total_3p_p'] = [u.p(total_wins, total), u.p(total_losses, total), u.p(total_wins, total_losses)]
    return results


def get_variant_types():
    with open(f'resources/variant_types.txt', 'r') as f:
        variants = {}
        for line in f.readlines():
            line = line.rstrip().split('\t')
            (key, val) = line[0], line[2]
            variants[key] = val
    return variants


def group_stats_by_eff(stats):
    variants = get_variant_types()
    list_easy = [row for row in stats if variants[row['options']['variantName']] == 'easy']
    list_null = [row for row in stats if variants[row['options']['variantName']] == 'null']
    list_sd = [row for row in stats if variants[row['options']['variantName']] == 'sd']
    list_dd = [row for row in stats if variants[row['options']['variantName']] == 'dd']
    return stats, list_easy, list_null, list_sd, list_dd


def get_all_stats(items):
    stats, list_easy, list_null, list_sd, list_dd = group_stats_by_eff(items)
    return {
        'Totals': get_totals(stats),
        'Easy': get_totals(list_easy),
        'Null': get_totals(list_null),
        'Single dark': get_totals(list_sd),
        'Double dark': get_totals(list_dd)
    }


def get_games_by_month(stats):
    stats = u.clear_2p(stats)
    months = {}
    for game in stats:
        d_game = game['datetimeFinished'][:7]
        if d_game in months:
            months[d_game] += 1
        else:
            months[d_game] = 1
    return dict(sorted(months.items()))

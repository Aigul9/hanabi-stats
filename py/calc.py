class UserStat:
    def __init__(self, game_id, count, score, variant, date, players, other_scores, suits, max_score):
        self.game_id = game_id
        self.count = count
        self.score = score
        self.variant = variant
        self.date = date
        self.players = players
        self.other_scores = other_scores
        self.suits = suits
        self.max_score = max_score


def p(value, total):
    if total != 0:
        return round(value * 100 / total, 2)
    else:
        return 0


def get_wins(totals_list):
    return len([row for row in totals_list if row.score == row.max_score])


def get_losses(totals_list):
    return len([row for row in totals_list if row.score != row.max_score])


def get_totals(stat_list):
    results = {}
    # total - count
    total = len(stat_list)
    total_wins = get_wins(stat_list)
    total_losses = get_losses(stat_list)
    results['total_c'] = [total_wins, total_losses, total]
    # total - %
    results['total_p'] = [p(total_wins, total), p(total_losses, total), p(total_wins, total_losses)]
    # 2p - count
    list_2p = get_list_2p(stat_list)
    total = len(list_2p)
    total_wins = get_wins(list_2p)
    total_losses = get_losses(list_2p)
    results['total_2p_c'] = [total_wins, total_losses, total]
    # 2p - %
    results['total_2p_p'] = [p(total_wins, total), p(total_losses, total), p(total_wins, total_losses)]
    # 3p - count
    list_3p = get_list_3p(stat_list)
    total = len(list_3p)
    total_wins = get_wins(list_3p)
    total_losses = get_losses(list_3p)
    results['total_3p_c'] = [total_wins, total_losses, total]
    # 3p - %
    results['total_3p_p'] = [p(total_wins, total), p(total_losses, total), p(total_wins, total_losses)]
    return results


def get_list_2p(stat_list):
    return [row for row in stat_list if int(row.count) == 2]


def get_list_3p(stat_list):
    return [row for row in stat_list if int(row.count) != 2]


def open_stats(username):
    with open(f'../temp/{username}_stats.txt', 'r') as f:
        return [UserStat(*line.rstrip().split('\t')) for line in f.readlines()]


def get_variant_types():
    with open(f'../resources/variant_types.txt', 'r') as f:
        variants = {}
        for line in f.readlines():
            line = line.rstrip().split('\t')
            (key, val) = line[0], line[2]
            variants[key] = val
    return variants


def group_stats_by_eff(username):
    stats = open_stats(username)
    variants = get_variant_types()
    list_easy = [row for row in stats if variants[row.variant] == 'easy']
    list_sd = [row for row in stats if variants[row.variant] == 'sd']
    list_null = [row for row in stats if variants[row.variant] == 'null']
    list_dd = [row for row in stats if variants[row.variant] == 'dd']
    return stats, list_easy, list_sd, list_null, list_dd


def get_all_stats(username):
    stats, list_easy, list_sd, list_null, list_dd = group_stats_by_eff(username)
    totals = get_totals(stats)
    totals_easy = get_totals(list_easy)
    totals_sd = get_totals(list_sd)
    totals_null = get_totals(list_null)
    totals_dd = get_totals(list_dd)
    return {
        'Totals': totals,
        'Easy': totals_easy,
        'Null': totals_null,
        'Single dark': totals_sd,
        'Double dark': totals_dd
    }

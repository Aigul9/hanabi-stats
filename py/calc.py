import pandas as pd
import xlsxwriter


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


def get_percent(value_wins, value_losses, total_value):
    if total_value != 0:
        return round(value_wins * 100 / total_value, 2), round(value_losses * 100 / total_value, 2)
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
    results['total_p'] = get_percent(total_wins, total_losses, total)
    # 2p - count
    list_2p = get_list_2p(stat_list)
    total = len(list_2p)
    total_wins = get_wins(list_2p)
    total_losses = get_losses(list_2p)
    results['total_2p_c'] = [total_wins, total_losses, total]
    # 2p - %
    results['total_2p_p'] = get_percent(total_wins, total_losses, total)
    # 3p - count
    list_3p = get_list_3p(stat_list)
    total = len(list_3p)
    total_wins = get_wins(list_3p)
    total_losses = get_losses(list_3p)
    results['total_3p_c'] = [total_wins, total_losses, total]
    # 3p - %
    results['total_3p_p'] = get_percent(total_wins, total_losses, total)
    return results


def get_list_2p(stat_list):
    return [row for row in stat_list if int(row.count) == 2]


def get_list_3p(stat_list):
    return [row for row in stat_list if int(row.count) != 2]


def save_to_file(data, caption, username, writer, offset_x, offset_y):
    df1 = pd.DataFrame({'Count': ['wins', 'losses', 'total'], '2p': data['total_2p_c'], '3p+': data['total_3p_c'],
                        'Total': data['total_c']})
    df2 = pd.DataFrame(
        {'%': ['wins', 'losses'], '2p': data['total_2p_p'], '3p+': data['total_3p_p'], 'Total': data['total_p']})
    df1.to_excel(writer, sheet_name='stats', index=False, startrow=offset_x, startcol=offset_y)
    df2.to_excel(writer, sheet_name='stats', index=False, startrow=offset_x + 5, startcol=offset_y)
    workbook = writer.book
    worksheet = writer.sheets['stats']
    # border_fmt = workbook.add_format({'border': 1})
    if caption == 'Totals':
        worksheet.write(f'A{offset_x - 1}', username)
    worksheet.write(f'A{offset_x}', caption)
    # worksheet.conditional_format(xlsxwriter.utility.xl_range(
    #     offset_x,
    #     offset_y,
    #     offset_x + len(df1),
    #     offset_y + len(df1.columns) - 1),
    #     {'type': 'no_errors', 'format': border_fmt}
    # )
    # worksheet.write(f'A{offset_x}', caption)
    # offset_x += 5
    # worksheet.conditional_format(xlsxwriter.utility.xl_range(
    #     offset_x,
    #     offset_y,
    #     offset_x + len(df2),
    #     offset_y + len(df2.columns) - 1),
    #     {'type': 'no_errors', 'format': border_fmt}
    # )
    return offset_x + 5


def open_stats(username):
    with open(f'../temp/{username}_stat.txt', 'r') as f:
        return [UserStat(*line.rstrip().split('\t')) for line in f.readlines()]


def get_variant_types():
    with open(f'../other_files/variant_types.txt', 'r') as f:
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


def get_writer(filename):
    try:
        return pd.ExcelWriter(f'../user_files/{filename}_stats.xlsx', engine='xlsxwriter')
    except PermissionError:
        print("Access denied. Please, close the file.")
        exit()


def get_all_stats(username):
    stats, list_easy, list_sd, list_null, list_dd = group_stats_by_eff(username)
    totals = get_totals(stats)
    totals_easy = get_totals(list_easy)
    totals_sd = get_totals(list_sd)
    totals_null = get_totals(list_null)
    totals_dd = get_totals(list_dd)
    return totals, totals_easy, totals_sd, totals_null, totals_dd

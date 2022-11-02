import csv

from sqlalchemy import func, false, extract

from database.db_connect import session, Game
from py.utils import open_file, add_zero

if __name__ == "__main__":
    purples = open_file('../input/purples.txt')

    # players who have at least 240 games (20 per month) and who has played with any current purple member
    players = session.query(func.unnest(Game.players), func.count(Game.game_id)) \
        .distinct() \
        .filter(Game.players.op('&&')(purples)) \
        .group_by(func.unnest(Game.players)) \
        .having(func.count(Game.game_id) >= 100) \
        .all()

    results_pivot = {}
    players_final = []

    for p in players:
        p = p[0]

        # exclude purples
        if p in purples:
            continue

        # number of games grouped by a period
        grouped_games = session \
            .query(extract('year', Game.date_time_started),
                   extract('month', Game.date_time_started),
                   func.count(Game.game_id)) \
            .filter(Game.num_players != 2) \
            .filter(Game.speedrun == false()) \
            .filter(Game.players.any(p)) \
            .group_by(extract('year', Game.date_time_started),
                      extract('month', Game.date_time_started)) \
            .having(func.count(Game.game_id) >= 20) \
            .all()
        len_games = len(grouped_games)

        # if <= 20 games each month
        if len_games == 0:
            continue

        # if >= 1 year in total
        if len_games >= 12:
            year_month_list = [[i[0], i[1]] for i in grouped_games]
            year, month = 2022, 11

            # if >= 20 games are not played in the past 6 months
            if [year, month - 1] not in year_month_list\
                    and [year, month - 2] not in year_month_list \
                    and [year, month - 3] not in year_month_list \
                    and [year, month - 4] not in year_month_list \
                    and [year, month - 5] not in year_month_list \
                    and [year, month - 6] not in year_month_list:
                continue

            players_final.append([p, len_games])

            for i in grouped_games:
                year_month = '-'.join([str(i[0]).replace('.0', ''), str(add_zero(i[1])).replace('.0', '')])
                if year_month in results_pivot.keys():
                    results_pivot[year_month][p] = i[2]
                else:
                    results_pivot[year_month] = {p: i[2]}
            print('======', p, '-----', len_games)

    results_pivot = {k: v for k, v in sorted(results_pivot.items(), key=lambda x: x[0], reverse=True) if '2022' in k}
    print(results_pivot)

    with open('../output/misc/new_purples.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player', 'Total months', 'Games in 2022', *results_pivot.keys()])
        for p in players_final:
            player, total = p[0], p[1]
            line = [player, total]
            total_sum = 0
            for k in results_pivot.keys():
                count = results_pivot[k].get(player)
                if count is not None:
                    total_sum += count
                    line.append(count)
                else:
                    line.append('-')
            line.insert(2, total_sum)
            w.writerow(line)

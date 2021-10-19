import csv
from sqlalchemy import func

import py.utils as u
from database.db_connect import session, H, Game


players = session.query(H.player).all()

weights_easy = u.open_csv('weights_easy_.csv')
weights_hard = u.open_csv('weights_hard_.csv')

last_player = players.index(('will.i.am', ))

f_easy = open('weights_easy__.csv', 'w', encoding='UTF-8')
f_hard = open('weights_hard__.csv', 'w', encoding='UTF-8')

w_easy = csv.writer(f_easy)
w_hard = csv.writer(f_hard)

for p in players[last_player:]:
    player = p[0]
    easy_check = player in [r[0] for r in weights_easy]
    hard_check = player in [r[0] for r in weights_hard]

    if easy_check and hard_check:
        print(f'skip {player}')
        continue

    teammates = session.query(func.unnest(Game.players))\
        .filter(Game.players.any(player))\
        .distinct()\
        .all()

    for t in teammates:
        teammate = t[0]

        if player == teammate:
            continue

        easy_check = False
        hard_check = False

        if player in [r[1] for r in weights_easy]\
                and teammate in [r[0] for r in weights_easy]:
            easy_check = True

        if player in [r[1] for r in weights_hard]\
                and teammate in [r[0] for r in weights_hard]:
            hard_check = True

        if not easy_check:
            count_easy = session.query(Game.game_id)\
                .filter(Game.players.any(player))\
                .filter(Game.players.any(teammate))\
                .filter(Game.eff < 1.25)\
                .count()

            if count_easy != 0:
                w_easy.writerow([player, teammate, count_easy])
                print(f'easy,{player},{teammate},{count_easy}')
                weights_easy.append([player, teammate, count_easy])

        if not hard_check:
            count_hard = session.query(Game.game_id)\
                .filter(Game.players.any(player))\
                .filter(Game.players.any(teammate))\
                .filter(Game.eff >= 1.25)\
                .count()

            if count_hard != 0:
                w_hard.writerow([player, teammate, count_hard])
                print(f'hard,{player},{teammate},{count_hard}')
                weights_hard.append([player, teammate, count_hard])

f_easy.close()
f_hard.close()

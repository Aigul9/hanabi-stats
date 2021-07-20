import json

from database.db_connect import session, Game, GameAction
import py.utils as u


# players_sets = session.query(Game.players).all()
# players = set()
# for ps in players_sets:
#     players |= set(ps[0])
#
# players = sorted(players)
# with open(f'../output/hanabi_players.txt', 'w', encoding='utf-8') as file:
#     for p in players:
#         file.write(p)
#         file.write('\n')


hanabi_players = u.open_file('../output/hanabi_players2.txt')
with open(f'../output/stats.txt', 'a') as file:
    for p in hanabi_players:
        print(p)
        try:
            stats = u.open_stats(p)
        except json.decoder.JSONDecodeError:
            print('error', p)
            continue
        for s in stats:
            json.dump(s, file)
            file.write('\n')

# print(all_stats)

    # for s in sorted(all_stats, key=lambda x: x['id']):


from database.db_connect import session
from database.db_schema import Game, GameAction


players_sets = session.query(Game.players).all()
players = set()
for ps in players_sets:
    players |= set(ps[0])

players = sorted(players)
with open(f'../output/hanabi_players.txt', 'w', encoding='utf-8') as file:
    for p in players:
        file.write(p)
        file.write('\n')


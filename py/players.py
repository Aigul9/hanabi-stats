from py.constants import username


with open(f'../user_files/{username}_players.txt', 'r') as f:
    players = set()
    for line in f.readlines():
        players = players.union(line.strip().split(', '))

players.remove(username)

with open(f'../user_files/{username}_players.txt', 'w', encoding='utf-8') as f:
    for i in sorted(players, key=str.casefold):
        f.write('{}\n'.format(i))

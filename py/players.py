def create_players_set(username):
    with open(f'../temp/{username}_players.txt', 'r', encoding='utf-8') as f:
        players = set()
        for line in f.readlines():
            players = players.union(line.strip().split(', '))
    players.remove(username)
    return players


def save_players_list(players, username):
    with open(f'../temp/{username}_players.txt', 'w', encoding='utf-8') as f:
        for i in sorted(players, key=str.casefold):
            f.write('{}\n'.format(i))

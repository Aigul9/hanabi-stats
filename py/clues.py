import py.utils as u
from database.db_connect import session, Game, GameAction, Variant


users = u.open_file('../input/list_of_players_notes.txt')
# [game_id, player_count, clues]
results = {k: [] for k in users}
for user in users:
    print(user)
    games = session.query(Game, Variant) \
        .join(Variant) \
        .filter(Game.players.any(user)) \
        .filter(Game.speedrun == False) \
        .all()
    print(len(games))
    alice_wins = 0
    alice_games = 0
    not_alice_wins = 0
    not_alice_games = 0
    for g, v in games:
        game_id = g.game_id
        # print(game_id)
        players = g.players
        players_count = len(players)
        players = (players[g.starting_player:] + players[:g.starting_player])
        actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
        clues = {k: 0 for k in players}
        for i in range(len(actions)):
            if u.is_clued(actions[i]):
                clues[players[i % players_count]] += 1
        max_users = [k for k, v in clues.items() if v == max(clues.values())]
        if len(max_users) == 1 and max_users[0] == user:
            alice_games += 1
            if g.score == v.max_score:
                alice_wins += 1
        else:
            not_alice_games += 1
            if g.score == v.max_score:
                not_alice_wins += 1
    # results[user].append([game_id, players_count, clues[user]])
    formula = round((alice_wins / alice_games) / (not_alice_wins / not_alice_games), 2)
    results[user] = formula, alice_wins, alice_games, not_alice_wins, not_alice_games
    print(results[user])

    # for c in range(2, 7):
    #     with open(f'../output/clues/{user}_clues_{c}p.tsv', 'a', encoding='utf-8', newline='') as file:
    #         w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
    #         w.writerow(['Game id', 'Player count', 'Number of clues'])
    #         data = sorted([v for v in results[user] if v[1] == c], key=lambda x: -x[2])
    #         for r in data:
    #             w.writerow([*r])

u.save('../output/winrate/alice/clue_giver', u.sort(results, 0), [
        'Player',
        'Ratio',
        'Alice\'s wins',
        'Num games being Alice',
        '!Alice\'s wins',
        'Num games not being Alice'
])

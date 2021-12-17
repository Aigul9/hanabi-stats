from sqlalchemy import false

import py.utils as u
from database.db_connect import session, Game, Player


def get_alice_wr(username):
    """Gets number of games and wins played as both Alice and not Alice.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    dict
        Number of games and wins played as both Alice and not Alice, ratio of such games grouped by player
    """
    games = session.query(Game) \
        .filter(Game.players.any(username)) \
        .filter(Game.num_players != 2) \
        .filter(Game.speedrun == false()) \
        .all()

    alice_list = session.query(Game)\
        .filter(Game.players[Game.starting_player + 1] == username)\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == 'false')\
        .all()

    # num games overall
    total_games = len(games)
    # num wins overall
    total_wins = u.get_wins_db(games)
    # num games going first
    alice_games = len(alice_list)
    # num wins going first
    alice_wins = 0
    for alice_game in alice_list:
        if alice_game.score == u.get_max_score(alice_game.variant):
            alice_wins += 1
    # num game not going first
    bob_games = total_games - alice_games
    # num wins not going first
    bob_wins = total_wins - alice_wins
    formula = round((alice_wins / alice_games) / (bob_wins / bob_games), 2)
    return formula, alice_wins, alice_games, bob_wins, bob_games


if __name__ == "__main__":
    users = session.query(Player.player).all()
    alice_ratio_dict = {}
    for user in users:
        user = user[0]
        alice_ratio_dict[user] = get_alice_wr(user)

    u.save('../output/winrate/alice/starting_player', u.sort(alice_ratio_dict, 0), [
        'Player',
        'Ratio',
        'Alice\'s wins',
        'Alice\'s games',
        '!Alice\'s wins',
        '!Alice\'s games'
    ])

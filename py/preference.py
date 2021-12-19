from sqlalchemy import func, false

import py_no_doc.utils as u
from database.db_connect import session, Game, Player, Variant


def get_teammates(username):
    """Gets list of player's teammates.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    teammates_list : list
        List of teammates
    """
    teammates_list = session.query(func.unnest(Game.players))\
        .distinct()\
        .filter(Game.players.any(username))\
        .all()
    teammates_list = [player[0] for player in teammates_list]
    teammates_list.remove(username)
    return teammates_list


def get_teammate_winrate(username, teammates_list):
    """Gets winrate by a teammate.

    Parameters
    ----------
    username : str
        Player name
    teammates_list : list
        List of teammates

    Returns
    -------
    teammate_winrate_dict : dict
        Winrate by a teammate sorted by winrate in a descending order
    """
    teammate_winrate_dict = {}
    games = session.query(Game, Variant)\
        .join(Variant)\
        .filter(Game.players.any(username))\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == false())\
        .all()
    for teammate in teammates_list:
        # print(games[0].__table__.columns) - list of props
        games_count = len([game for game, variant in games if teammate in game.players])

        if games_count < 100:
            continue

        wins_count = len([game for game, variant in games if teammate in game.players
                          and game.score == variant.max_score])
        winrate = u.p(wins_count, games_count)
        teammate_winrate_dict[teammate] = winrate
    return u.sort_by_value(teammate_winrate_dict)


def get_preference(teammate_winrate_dict):
    """Calculates preference for each teammate.

    Parameters
    ----------
    teammate_winrate_dict : dict
        Winrate by a teammate sorted by winrate in a descending order

    Returns
    -------
        Preference by a teammate
    """
    teammate_preference_dict = {}
    teammates_count = len(teammate_winrate_dict)
    for teammate in teammate_winrate_dict.keys():
        teammate_preference_dict[teammate] =\
            (
                    teammates_count - list(teammate_winrate_dict.keys())
                    .index(teammate) - 1
            ) / teammates_count
    return teammate_preference_dict


def update_preference(player_teammate_preference, teammate_preference_dict):
    """Adds preferences of a current player to global dict of preferences.

    Parameters
    ----------
    player_teammate_preference : dict
        Global preference towards a teammate grouped by a player
    teammate_preference_dict : dict
        Preference towards a teammate for a current player

    Returns
    -------
    player_teammate_preference : dict
        Updated global preference towards a teammate grouped by a player
    """
    for teammate, preference in teammate_preference_dict.items():
        if teammate not in player_teammate_preference:
            player_teammate_preference[teammate] = {'preference': 0, 'lists_count': 0}
        else:
            player_teammate_preference[teammate]['preference'] += preference
            player_teammate_preference[teammate]['lists_count'] += 1
    return player_teammate_preference


def average_preference(player_preference):
    """Averages global dict of preferences.

    Parameters
    ----------
    player_preference : dict
        Preference towards a player

    Returns
    -------
    dict
        Averages preference towards a player
    """
    for player, preference in player_preference.items():
        try:
            player_preference[player] = round(preference['preference'] / preference['lists_count'], 2)
        except ZeroDivisionError:
            player_preference[player] = -1
    return {player: preference for player, preference in player_preference.items() if player in users}


if __name__ == "__main__":
    users = session.query(Player.player).all()
    users = [user[0] for user in users]
    users_preference = {k: {'preference': 0, 'lists_count': 0} for k in users}
    for user in users:
        teammates = get_teammates(user)
        teammate_winrate = get_teammate_winrate(user, teammates)
        teammate_preference = get_preference(teammate_winrate)
        users_preference = update_preference(users_preference, teammate_preference)

    users_preference = average_preference(users_preference)
    u.save_header('../output/ratio/preference1', ['Username', 'Preference'])
    u.save_value('../output/ratio/preference1', u.sort_by_value(users_preference))

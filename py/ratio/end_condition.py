"""
Description:
    Percentage of terminated, strikeout, timeout, and normal games in player's history
    sorted by terminated games in descending order.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - Terminated: percentage of terminated games
    - Strikeout: percentage of strikeout games
    - Timeout: percentage of timeout games
    - Normal: percentage of normally finished games
"""

import csv
from sqlalchemy import false

import py.utils as u
from database.db_connect import session, Game, Player


def sort_terminated(condition_count_dict):
    """Sorts players by number of terminated games in descending order.

    Parameters
    ----------
    condition_count_dict : dict
        Number of games grouped by an end condition

    Returns
    -------
        dict
        Sorted input dictionary
    """
    return {k: v for k, v in sorted(condition_count_dict.items(), key=lambda x: -x[1][4] / x[1]['total'])}


def sort_strikeout(condition_count_dict):
    """Sorts players by number of strikeout games in descending order.

    Parameters
    ----------
    condition_count_dict : dict
        Number of games grouped by an end condition

    Returns
    -------
        dict
        Sorted input dictionary
    """
    return {k: v for k, v in sorted(condition_count_dict.items(), key=lambda x: -x[1][2])}


def save(condition_count_dict):
    """Saves total number of games grouped by player and end condition.

    Parameters
    ----------
    condition_count_dict : dict
        Number of games grouped by an end condition
    """
    with open('../../output/ratio/end_condition.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t')
        w.writerow([
            'Player',
            # 4
            'Terminated',
            # 2
            'Strikeout',
            # 3
            'Timeout',
            # 1
            'Normal'
        ])
        for k, v in condition_count_dict.items():
            t = v['total']
            w.writerow([
                k,
                f'{u.p(v[4], t)}',
                f'{u.p(v[2], t)}',
                f'{u.p(v[3], t)}',
                f'{u.p(v[1], t)}'
            ])


def count_conditions(username):
    """Calculates number of games for each end condition.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    condition_count_dict : dict
        Number of games grouped by an end condition
    """
    condition_count_dict = {i: 0 for i in range(11)}
    games = session.query(Game) \
        .filter(Game.players.any(username)) \
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == false())\
        .all()
    for game in games:
        ec = game.end_condition
        condition_count_dict[ec] += 1
    condition_count_dict['total'] = len(games)
    return condition_count_dict


if __name__ == "__main__":
    users = session.query(Player.player).all()
    users_conditions = {}

    for user in users:
        user = user[0]
        users_conditions[user] = count_conditions(user)

    save(sort_terminated(users_conditions))

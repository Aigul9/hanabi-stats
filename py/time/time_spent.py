import csv
from itertools import groupby

import py.utils as u
from database.db_connect import session, Game, Player


def save(player_times_dict):
    """Saves total time spent on games by player into a tsv file.

    Parameters
    ----------
    player_times_dict : dict
        Total days, hours, minutes per game, hours per day by player
    """
    with open(f'../../output/time/times_spent.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(
            ['Player', 'Days', 'Per game (in min)', 'Per day (in h)'])
        for k, v in player_times_dict.items():
            w.writerow([k, v[0]['days'], v[1], v[2]])


def group_stats(games):
    """Calculates number of days spent on the website.

    Parameters
    ----------
    games : list
        Player's games

    Returns
    -------
    int
        Number of days
    """
    groups = groupby(games, lambda row: row.date_time_finished.date())
    return len(list(groups))


def get_times(username):
    """Calculates number of minutes per game and hours per day.


    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    times : list
        Total seconds, minutes per game and hours per day
    """
    games = session.query(Game) \
        .filter(Game.players.any(username))\
        .order_by(Game.game_id)\
        .all()
    days = group_stats(games)
    times = [0, len(games), days]
    for game in games:
        diff = game.date_time_finished - game.date_time_started
        times[0] += diff.total_seconds()
    # per game
    times[1] = times[0] / times[1] / 60
    # per day excl. days with 0 games
    times[2] = times[0] / times[2] / 3600
    return times


if __name__ == "__main__":
    users = session.query(Player.player).all()
    users_times = {}
    for user in users:
        user = user[0]
        users_times[user] = get_times(user)

    users_times = {k: [
        u.convert_sec_to_day(v[0]),
        round(v[1]),
        round(v[2], 1)
    ]
        for k, v in u.sort(users_times, 0).items()}
    save(users_times)

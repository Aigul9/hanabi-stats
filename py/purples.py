import csv
from sqlalchemy import false

import py_no_doc.utils as u
from database.db_connect import session, Game, Player


def get_purples_dates():
    """Gets the date when a player became purple.

    Returns
    -------
    player_purple_date_dict : dict
        A dictionary in format: "player: date"
    """
    purples_list = u.open_file('../input/purples.txt')
    player_purple_date_dict = {}
    for player in purples_list:
        date = session.query(Game.date_time_started)\
            .filter(Game.players.any(player))\
            .order_by(Game.game_id)\
            .first()[0]
        date = date.replace(year=date.year + 1)
        player_purple_date_dict[player] = date
    return player_purple_date_dict


def count_purple_games(username, player_purple_date_dict):
    """Calculates number of games with purple players.

    Parameters
    ----------
    username : str
        Player name
    player_purple_date_dict : dict
        Player names and dates when they became purple

    Returns
    -------
    purple_games_count : int
        Number of games with purple players
    """
    games = session.query(Game)\
        .filter(Game.players.any(username))\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == false())\
        .all()

    purple_games_count = 0

    for game in games:
        game_date = game.date_time_finished
        for player in game.players:
            if (
                    player != username and
                    player in player_purple_date_dict.keys() and
                    player_purple_date_dict[player] < game_date
            ):
                purple_games_count += 1
                break

    return purple_games_count


def save_purples(purples_count_dict):
    """Saves number of games with purple players into a tsv file.

    Parameters
    ----------
    purples_count_dict : dict
        Number of games by player
    """
    with open(f'../output/misc/purples.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Players', '# with purples'])
        for k, v in sorted(purples_count_dict.items(), key=lambda row: -row[1]):
            w.writerow([k, v])


if __name__ == "__main__":
    purples_dates = get_purples_dates()
    users = session.query(Player.player).all()
    purples = {}
    for user in users:
        user = user[0]
        purples[user] = count_purple_games(user, purples_dates)
    save_purples(purples)

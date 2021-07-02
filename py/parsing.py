import errno
import requests
import os


def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


def export_game(game):
    url = f'https://hanab.live/export/{game["id"]}'
    response = requests.get(url)
    return response.json()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_players_set(items, username):
    players = set()
    for item in items:
        players = players.union(item['playerNames'])
    players.remove(username)
    return players

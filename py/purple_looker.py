"""
Description:
    Number of games grouped by a year and a month in order to identify suitable green players for a purple role.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Month: month
    - Year: year
    - Games: total number of games
"""

import requests
import csv
import calendar
from itertools import groupby


def open_stats(user):
    """Gets user's statistics from the history page.

    Parameters
    ----------
    user : str
        Player name

    Returns
    -------
    list
        History in json format
    """
    url = f'https://hanab.live/api/v1/history-full/{user}'
    response = requests.get(url)
    return response.json()


def clear_2p(stats):
    """Removes 2-player games from the user's statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History without 2-player games
    """
    return [row for row in stats if int(row['options']['numPlayers']) != 2]


def clear_speedruns(stats):
    """Removes speedruns from the user's statistics.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    list
        History without speedruns
    """
    return [row for row in stats if not row['options']['speedrun']]


def group_stats(stats):
    """Groups user's games by year and month.

    Parameters
    ----------
    stats : list
        User's games

    Returns
    -------
    dict
        Number of games grouped by a period
    """
    groups = groupby(stats, lambda row: row['datetimeFinished'][:7])
    grouped_stats = {}
    for k, v in groups:
        group = list(v)
        grouped_stats[k] = len(group)
    return {k: v for k, v in sorted(grouped_stats.items())}


def save(grouped_stats, user):
    """Saves grouped user's statistics into a tsv file.

    Parameters
    ----------
    grouped_stats : dict
        Number of games grouped by a period
    user : str
        Player name
    """
    with open(f'../output/misc/{user}.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['month', 'year', 'games'])
        for k, v in grouped_stats.items():
            month = calendar.month_abbr[int(k[5:])]
            year = k[:4]
            w.writerow([month, year, f'{v} games'])
        w.writerow([f'Total: {sum(grouped_stats.values())}', '', ''])


if __name__ == "__main__":
    username = 'Lanvin'
    data = group_stats(clear_2p(clear_speedruns(open_stats(username))))
    save(data, username)

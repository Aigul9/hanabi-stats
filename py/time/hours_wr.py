"""
Description:
    Winrate of each player by hour sorted by player and hour in ascending order.
    It is calculated as a number of games in which the score equals to a max score
    divided by the total number of games.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - Hour: an hour
    - WR: winrate
    - Wins: number of games won
    - Games: number of total games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/time/hours_wr'
    header = ['Player', 'Hour', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)

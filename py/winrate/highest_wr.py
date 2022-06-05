"""
Description:
    Winrate of each player sorted in descending order. It is calculated as a number of games in which the score equals to a max score
    divided by the total number of games.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - WR: winrate
    - Wins: number of games won
    - Games: number of total games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/highest_wr'
    header = ['Player', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)

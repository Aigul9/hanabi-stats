"""
Description:
    Winrate of a pair of players who have more than 50 games in common sorted by player in ascending order
    and WR in descending order.
    It is calculated as a number of games in which the score equals to a max score divided by the total number of games.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - Teammate: teammate name
    - WR: winrate
    - Wins: number of games won
    - Games: number of total games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/teammates_wr'
    header = ['Player', 'Teammate', 'WR', 'Wins', 'Games']
    u.run_workflow(path, header)

"""
Description:
    Number of terminated 2p games sorted by percentage in descending order.

Exclusions:
    - speedruns

Columns:
    - Player1: player name
    - Player2: player name
    - Total: total number of games for the pair of players
    - Terminated: number of terminated games
    - %: percentage of terminated games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/terminated_2p'
    header = ['Player1', 'Player2', 'Total', 'Terminated', '%']
    u.run_workflow(path, header)

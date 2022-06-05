"""
Description:
    Number and percentage of games grouped by number of suits and sorted by player in ascending order.

Exclusions:
    - 2p games
    - speedruns
    - No Variant

Columns:
    - Player: player name
    - 6 suits: number of 6 suits games
    - 6 suits %: percentage of 6 suits games
    - 5 suits: number of 5 suits games
    - 5 suits %: percentage of 5 suits games
    - 4 suits: number of 4 suits games
    - 4 suits %: percentage of 4 suits games
    - 3 suits: number of 3 suits games
    - 3 suits %: percentage of 3 suits games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/suits_distribution'
    header = ['Player',
              '6 suits', '6 suits %',
              '5 suits', '5 suits %',
              '4 suits', '4 suits %',
              '3 suits', '3 suits %']
    u.run_workflow(path, header)

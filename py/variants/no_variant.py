"""
Description:
    Number of 'No Variant' games in each player's history sorted in descending order.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - Count: number of 'No Variant' games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/variants/no_variant'
    header = ['Player', 'Count']
    u.run_workflow(path, header)

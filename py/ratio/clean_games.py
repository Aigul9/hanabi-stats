"""
Description:
    Percentage of games without any misplays sorted in descending order.

Exclusions:
    - 2p games
    - speedruns
    - detrimental characters
    - all or nothing
    - one extra card
    - one less card
    - No Variant

Columns:
    - Player: player name
    - %: percentage of clean games
    - Clean: number of games without any misplays
    - Total: total number of games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/clean_games'
    header = ['Player', '%', 'Clean', 'Total']
    u.run_workflow(path, header)

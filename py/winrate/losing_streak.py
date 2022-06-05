"""
Description:
    Losing streak sorted by count in descending order.

Exclusions:
    - speedruns

Columns:
    - Player: player name
    - Count: number of games lost in a row
    - Start game_id: Game id the streak starts with
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/winrate/losing_streak'
    header = ['Player', 'Count', 'Start game_id']
    u.run_workflow(path, header)

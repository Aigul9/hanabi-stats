"""
Description:
    Percentage of games in which the action from the player led to a strikeout sorted in descending order.
    It represents the player's responsibility for losing the game.

Exclusions:
    - 2p games
    - speedruns

Columns:
    - Player: player name
    - %: percentage of games in which the last bomb from the player led to a strikeout
    - Third strike: number of third strikes
    - Total: total number of strikeout games
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/ratio/risky_players'
    header = ['Player', '%', 'Third strike', 'Total']
    u.run_workflow(path, header)

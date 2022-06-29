"""
Description:
    BDR distribution by player in normal or strikeout games.

Exclusions:
    - 2p games
    - speedruns
    - detrimental characters
    - end condition other than normal and strikeout

Columns:
    - Player: player name
    - Max BDR: max BDR
    - n BDR %: percentage of n BDR
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/bdr/bdr_distribution'
    header = [
        'Player',
        'Max BDR',
        '0 BDR %',
        '1 BDR %',
        '2 BDR %',
        '3 BDR %',
        '4 BDR %',
        '5 BDR %',
        '6 BDR %',
        '7 BDR %',
        '8 BDR %',
        '9 BDR %',
        '10 BDR %']
    u.run_workflow(path, header)

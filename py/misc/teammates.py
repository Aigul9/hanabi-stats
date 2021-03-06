"""
Description:
    Number of distinct teammates sorted in descending order.

Columns:
    - Player: player name
    - Teammates: number of distinct teammates
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/misc/teammates'
    header = ['Player', 'Teammates']
    u.run_workflow(path, header)

"""
Description:
    Year and month for each player when they spent the max number of hours on the website
    sorted by a player in ascending order.
    It is calculated as a sum of differences between game end time and game start time
    grouped by year and month.

Columns:
    - Player: player name
    - Year: year
    - Month: month
    - Hours: amount of hours
"""

import py.utils as u


if __name__ == "__main__":
    path = 'output/time/peaks'
    header = ['Player', 'Year', 'Month', 'Hours']
    # TODO: fix 2020 instead of 2020.0
    u.run_workflow(path, header)

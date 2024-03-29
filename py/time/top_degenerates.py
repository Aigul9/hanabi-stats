"""
Description:
    List of top players spent the most amount of time online.
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
    path = 'output/time/top_degenerates'
    header = ['Player', 'Year', 'Month', 'Hours']
    u.run_workflow(path, header)

"""
Description:
    List of top 10 players spent the most amount of time online in a month.
    It is calculated as a sum of differences between game end time and game start time.

Columns:
    - Player: player name
    - Hours: amount of hours
"""

from datetime import datetime

from sqlalchemy import text

import py.utils as u

if __name__ == "__main__":
    path = 'output/time/monthly_hanabaddicts'
    header = ['Player', 'Hours']
    date = datetime.now()  # .replace(2022, 9)
    month = date.month
    year = date.year
    sub_path = f'output/time/monthly_hanabaddicts/{year}_{date.strftime("%m")}'

    sql_file = u \
        .read_file(f'../../database/sql/{path}.sql') \
        .replace('cur_year', str(year)) \
        .replace('cur_month', str(month))
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../{sub_path}', header)
    u.save_list_tsv(f'../../{sub_path}', result)

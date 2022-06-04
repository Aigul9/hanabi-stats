from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'peaks'
    sql_file = u.read_file(f'../../database/sql/output/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    # TODO: fix 2020 instead of 2020.0
    u.save_header(f'../../output/time/{filename}', ['Player', 'Year', 'Month', 'Hours'])
    u.save_list_tsv(f'../../output/time/{filename}', result)

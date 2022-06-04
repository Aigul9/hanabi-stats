from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'misplays'
    sql_file = u.read_file(f'../../../database/sql/output/pmdc/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../../output/ratio/pmdc/{filename}', ['Player', 'Ratio', 'Misplays', 'Games'])
    u.save_list_tsv(f'../../../output/ratio/pmdc/{filename}', result)

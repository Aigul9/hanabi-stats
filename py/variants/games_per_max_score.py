from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'games_per_max_score'
    sql_file = u.read_file(f'../../database/sql/output/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../output/variants/{filename}', ['Variant', 'Variant id', 'Games', 'Total', 'Max scores'])
    u.save_list_tsv(f'../../output/variants/{filename}', result)

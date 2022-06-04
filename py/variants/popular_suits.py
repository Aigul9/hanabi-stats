from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'popular_suits'
    sql_file = u.read_file(f'../../database/sql/output/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../output/variants/{filename}', ['Suit', 'Count', '%'])
    u.save_list_tsv(f'../../output/variants/{filename}', result)

from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'notes_count'
    sql_file = u.read_file(f'../../database/sql/output/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../output/notes/{filename}', ['Player', 'Ratio', 'Games', 'Notes'])
    u.save_list_tsv(f'../../output/notes/{filename}', result)

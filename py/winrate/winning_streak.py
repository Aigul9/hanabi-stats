from sqlalchemy import text

import py.utils as u


if __name__ == "__main__":
    filename = 'winning_streak'
    sql_file = u.read_file(f'../../database/sql/output/{filename}.sql')
    sql = text(sql_file)
    result = u.run_query(sql)
    u.save_header(f'../../output/winrate/{filename}', ['Player', 'Count', 'Start game_id'])
    u.save_list_tsv(f'../../output/winrate/{filename}', result)

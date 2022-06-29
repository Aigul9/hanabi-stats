"""
Description:
    List of games with BDR for a specific player.

Exclusions:
    - 2p games
    - speedruns
    - detrimental characters
    - end condition other than normal and strikeout

Columns:
    - Player: player name
    - Game id: game id
    - Variant: variant name
    - BDR: bottom deck risk
"""

from sqlalchemy import text

import py.utils as u
from database.db_connect import session, Player


if __name__ == "__main__":
    users = session.query(Player.player).all()
    path = 'output/bdr/players/bdr_list'
    header = ['Player', 'Game id', 'Variant', 'BDR']
    for user in users:
        user = user[0]
        sql_file = u.read_file(f'../../database/sql/{path}.sql').replace('player_name', user)
        sql = text(sql_file)
        result = u.run_query(sql)
        u.save_header(f'../../{path}_{user}', header)
        u.save_list_tsv(f'../../{path}_{user}', result)
        print(user)

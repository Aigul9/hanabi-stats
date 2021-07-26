from sqlalchemy import and_

from py.utils import logger
from database.db_connect import session, Game, CardAction
from database.db_load import update_misplays


games = session.query(
    Game
) \
    .join(CardAction) \
    .filter(
    and_(
        Game.game_id >= 159000,
        Game.game_id <= 209000
    )
)\
    .distinct(Game.game_id)\
    .order_by(Game.game_id)\
    .all()

# .filter(Game.game_id == 186841).all()
for game in games:
    logger.info(game.game_id)
    update_misplays(game)
    session.commit()
session.close()

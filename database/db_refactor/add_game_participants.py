from database.db_connect import session, Game, GameParticipant
from py.utils import logger

games = session.query(Game.game_id, Game.players, Game.starting_player).order_by(Game.game_id).all()

for game in games:
    game_id, players, starting_player = game
    num_players = len(players)
    for i in range(num_players):
        players_mod = players[starting_player:] + players[:starting_player]
        game_participant = GameParticipant(game_id, players_mod[i], i)
        session.add(game_participant)
    session.commit()
    logger.info(game_id)

session.close()

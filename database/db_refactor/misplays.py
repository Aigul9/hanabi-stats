import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, Variant, CardAction


games = session.query(
    Game.game_id,
    Game.variant
) \
    .join(CardAction) \
    .distinct(Game.game_id)\
    .order_by(Game.game_id)\
    .all()

# TODO: select misplays > 3
for game_id, variant in games:
    logger.info(game_id)
    game_card_actions = session.query(CardAction)\
        .filter(CardAction.game_id == game_id)\
        .order_by(CardAction.turn_action)\
        .all()
    suits = session.query(Variant.suits).filter(Variant.variant == variant).scalar()
    piles = [0] * u.get_number_of_suits(variant)
    for card_action in game_card_actions:
        if card_action.action_type in ['play', 'misplay']:
            card_suit_ind = suits.index(card_action.card_suit)
            if not u.is_played(piles, card_suit_ind, card_action.card_rank):
                card_action.action_type = 'misplay'
            else:
                card_action.action_type = 'play'
                piles[card_suit_ind] = card_action.card_rank
    session.commit()
session.close()

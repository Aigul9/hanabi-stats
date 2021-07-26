from sqlalchemy import and_

import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, Variant, CardAction


games = session.query(
    Game.game_id,
    Game.variant
) \
    .join(CardAction) \
    .filter(
    and_(
        Game.game_id >= 130000,
        Game.game_id <= 144000
    )
)\
    .distinct(Game.game_id)\
    .order_by(Game.game_id)\
    .all()

# .filter(Game.game_id == 186841).all()


# TODO: select misplays > 3
for game_id, variant in games:
    logger.info(game_id)
    game_card_actions = session.query(CardAction)\
        .filter(CardAction.game_id == game_id)\
        .order_by(CardAction.turn_action)\
        .all()
    suits = session.query(Variant.suits).filter(Variant.variant == variant).scalar()
    if 'Up or Down' in variant:
        piles = [[0, '']] * u.get_number_of_suits(variant)
    else:
        piles = [[0, 'up']] * u.get_number_of_suits(variant)
        if 'Reversed' in variant:
            piles[len(suits) - 1] = [6, 'down']
    for card_action in game_card_actions:
        if card_action.action_type in ['play', 'misplay']:
            card_suit_ind = suits.index(card_action.card_suit)
            if not u.is_played(piles, card_suit_ind, card_action.card_rank):
                card_action.action_type = 'misplay'
            else:
                card_action.action_type = 'play'
                piles[card_suit_ind] = [
                    card_action.card_rank,
                    u.up_or_down_direction(piles, card_suit_ind, card_action.card_rank)
                ]
    session.commit()
session.close()

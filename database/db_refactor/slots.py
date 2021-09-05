from sqlalchemy import and_, desc, func, or_, false

import database.db_load as d
import py.utils as u
from database.db_connect import session, Game, CardAction, Slot


games = session.query(
    Game.game_id,
    Game.num_players,
    Game.one_less_card,
    Game.one_extra_card
) \
    .filter(Game.game_id == 2907)\
    .filter(Game.card_cycle == false())\
    .order_by(Game.game_id)\
    .all()

for g in games:
    card_actions = session.query(CardAction)\
        .filter(and_(
            CardAction.game_id == g.game_id,
            CardAction.turn_drawn != None
    ))\
        .order_by(CardAction.card_index)\
        .all()
    len_cards = u.get_number_of_cards_in_hand(g.num_players, g.one_less_card, g.one_extra_card)
    for ca in card_actions:
        if ca.turn_drawn == 0:
            slot = len_cards - ca.card_index % len_cards
        else:
            slot = 1
        d.load_slots(ca, ca.turn_drawn, slot)
    card_actions = [ca for ca in card_actions if ca.turn_action is not None]
    for ca in sorted(card_actions, key=lambda x: x.turn_action):
        card_slot = session.query(func.max(Slot.slot)).filter(
            and_(Slot.game_id == ca.game_id,
                 Slot.card_index == ca.card_index)
        ).scalar()
        card_actions_join_slots = session.query(CardAction)\
            .join(Slot)\
            .filter(and_(
                CardAction.turn_drawn < ca.turn_action,
                CardAction.player == ca.player,
                CardAction.card_index != ca.card_index
        ))\
            .filter(or_(
                CardAction.turn_action > ca.turn_action,
                CardAction.turn_action == None
        ))\
            .order_by(desc(CardAction.card_index))\
            .all()[:card_slot - 1]
        for i in range(len(card_actions_join_slots)):
            d.load_slots(card_actions_join_slots[i], ca.turn_action, i + 2)
    d.session.commit()

d.session.close()

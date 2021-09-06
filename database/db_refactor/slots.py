import copy
from sqlalchemy import and_, func, false

import database.db_load as d
import py.utils as u
from database.db_connect import session, Game, CardAction, Slot
from py.utils import logger


last_id = d.session.query(func.max(Slot.game_id)).scalar()
games = session.query(
    Game.game_id,
    Game.num_players,
    Game.one_less_card,
    Game.one_extra_card
) \
    .filter(
    and_(
        Game.card_cycle == false(),
        Game.game_id > last_id
    ))\
    .order_by(Game.game_id)\
    .all()

for g in games:
    logger.info(g.game_id)
    card_actions = session.query(CardAction)\
        .filter(and_(
            CardAction.game_id == g.game_id,
            CardAction.turn_drawn != None
    ))\
        .order_by(CardAction.card_index)\
        .all()
    card_actions_copy = copy.deepcopy(card_actions)
    len_cards = u.get_number_of_cards_in_hand(g.num_players, g.one_less_card, g.one_extra_card)
    slots = []
    for ca in card_actions:
        if ca.turn_drawn == 0:
            slot = len_cards - ca.card_index % len_cards
        else:
            slot = 1
        slots.append(d.load_slots(ca, ca.turn_drawn, slot))
    card_actions = [ca for ca in card_actions if ca.turn_action is not None]
    for ca in sorted(card_actions, key=lambda x: x.turn_action):
        card_slot = max([s.slot for s in slots if s.card_index == ca.card_index])
        card_actions_join_slots = sorted([
            a for a in card_actions_copy if
            a.turn_drawn < ca.turn_action and
            a.player == ca.player and
            a.card_index != ca.card_index and
            (a.turn_action is None or
             a.turn_action > ca.turn_action)
        ], key=lambda x: -x.card_index)[:card_slot - 1]
        for i in range(len(card_actions_join_slots)):
            slots.append(d.load_slots(card_actions_join_slots[i], ca.turn_action, i + 2))
    d.session.commit()

d.session.close()

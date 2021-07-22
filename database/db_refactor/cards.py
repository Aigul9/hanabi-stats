import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, GameAction, Card, Variant, CardAction, Clue


games = session.query(Game)\
    .join(CardAction, isouter=True)\
    .filter(CardAction.game_id == None)\
    .all()
actions_q = session.query(GameAction)
decks_q = session.query(Card)
variants_q = session.query(Variant)
game_card_actions_q = session.query(CardAction)
logger.info(len(games))
for game in games:
    logger.info(game.game_id)
    game_card_actions = game_card_actions_q\
        .filter(CardAction.game_id == game.game_id)
    actions = actions_q.filter(GameAction.game_id == game.game_id).all()
    deck = decks_q.filter(Card.seed == game.seed).all()
    variant = variants_q.filter(Variant.variant_id == game.variant_id).first()
    players = (game.players[game.starting_player:] + game.players[:game.starting_player])
    current_card_ind = u.get_number_of_starting_cards(game.num_players, game.one_less_card, game.one_extra_card)
    cards_per_hand = u.get_number_of_cards_in_hand(game.num_players, game.one_less_card, game.one_extra_card)
    for card in deck:
        new_card_action = CardAction(
            card.card_index,
            game.game_id,
            variant.suits[card.suit_index],
            card.rank,
            None,
            None,
            None,
            None
        )
        session.add(new_card_action)
    for i in range(current_card_ind):
        player = players[i // cards_per_hand]
        card_action = game_card_actions\
            .filter(CardAction.card_index == i)\
            .first()
        card_action.player = player
        card_action.turn_drawn = 0
    for action in actions:
        if u.is_clued(action):
            # color
            if action.action_type == 2:
                try:
                    value = variant.colors[action.value]
                except IndexError:
                    logger.error(f'{action.value}, {variant.colors}')
            # rank
            else:
                value = action.value
            clue = Clue(
                action.turn + 1,
                game.game_id,
                value,
                'color' if action.action_type == 2 else 'rank',
                players[action.turn % game.num_players],
                players[action.target]
            )
            session.add(clue)
        elif action.action_type in [0, 1]:
            types = {
                0: 'play',
                1: 'discard'
            }
            card_action = game_card_actions\
                .filter(CardAction.card_index == action.target)\
                .first()
            card_action.action_type = types[action.action_type]
            card_action.turn_action = action.turn + 1

            if current_card_ind == len(deck):
                continue
            next_card_action = game_card_actions\
                .filter(CardAction.card_index == current_card_ind)\
                .first()
            next_card_action.turn_drawn = action.turn + 1
            next_card_action.player = players[action.turn % game.num_players]
            current_card_ind += 1
    session.commit()
session.close()

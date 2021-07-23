import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, GameAction, Card, Variant, CardAction, Clue


games = session.query(
    Game.game_id,
    Game.seed,
    Game.players,
    Game.num_players,
    Game.variant_id,
    Game.starting_player,
    Game.one_less_card,
    Game.one_extra_card
)\
    .join(CardAction, isouter=True) \
    .filter(CardAction.game_id == None)\
    .all()
actions_q = session.query(GameAction)
decks_q = session.query(Card)
variants_q = session.query(Variant.suits, Variant.colors)
game_card_actions_q = session.query(CardAction)
for game_id, seed, players, num_players, variant_id, starting_player,\
        one_less_card, one_extra_card in games:
    logger.info(game_id)
    game_card_actions = game_card_actions_q\
        .filter(CardAction.game_id == game_id)
    actions = actions_q.filter(GameAction.game_id == game_id).all()
    deck = decks_q.filter(Card.seed == seed).all()
    suits, colors = variants_q.filter(Variant.variant_id == variant_id).first()
    players_orig = players
    players_mod = (players[starting_player:] + players[:starting_player])
    current_card_ind = u.get_number_of_starting_cards(num_players, one_less_card, one_extra_card)
    cards_per_hand = u.get_number_of_cards_in_hand(num_players, one_less_card, one_extra_card)
    for card in deck:
        new_card_action = CardAction(
            card.card_index,
            game_id,
            suits[card.suit_index],
            card.rank,
            None,
            None,
            None,
            None
        )
        session.add(new_card_action)
    for i in range(current_card_ind):
        player = players_mod[i // cards_per_hand]
        card_action = game_card_actions\
            .filter(CardAction.card_index == i)\
            .first()
        card_action.player = player
        card_action.turn_drawn = 0
    # TODO: update clues for games where starting player != 0 (~ id < 11k)
    for action in actions:
        if u.is_clued(action):
            # color
            if action.action_type == 2:
                try:
                    value = colors[action.value]
                except IndexError:
                    logger.error(f'{action.value}, {colors}')
            # rank
            else:
                value = action.value
            clue = Clue(
                action.turn + 1,
                game_id,
                value,
                'color' if action.action_type == 2 else 'rank',
                players_mod[action.turn % num_players],
                players_orig[action.target]
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
            next_card_action.player = players_mod[action.turn % num_players]
            current_card_ind += 1
    session.commit()
session.close()

import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, GameAction, Card, Variant, CardAction, Clue


# mod_actions_ids = u.open_file('../../temp/clues_games.txt')
# for m in u.open_file('../../temp/mod card_actions.txt'):
#     mod_actions_ids.append([int(s) for s in m.split() if s.isdigit()][0])
#
for g_id in [9524]:
    game_id, seed, players, num_players, variant_id, starting_player, one_less_card, one_extra_card =\
        session.query(
            Game.game_id,
            Game.seed,
            Game.players,
            Game.num_players,
            Game.variant_id,
            Game.starting_player,
            Game.one_less_card,
            Game.one_extra_card
        )\
            .join(CardAction)\
            .filter(Game.game_id == g_id)\
            .first()
# for game_id, seed, players, num_players, variant_id, starting_player, one_less_card, one_extra_card in games:
    logger.info(game_id)
    game_card_actions = session.query(CardAction).filter(CardAction.game_id == game_id)
    actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
    len_deck = session.query(Card).filter(Card.seed == seed).count()
    players_orig = players
    players_mod = (players[starting_player:] + players[:starting_player])
    current_card_ind = u.get_number_of_starting_cards(num_players, one_less_card, one_extra_card)

    for action in actions:
        if u.is_clued(action):
            clue = session.query(Clue).filter(Clue.game_id == game_id) \
                .filter(Clue.turn_clued == action.turn + 1).first()
            clue.clue_giver = players_mod[action.turn % num_players]
            clue.clue_receiver = players_orig[action.target]
        elif action.action_type == 4:
            break
        elif action.action_type in [0, 1]:
            if current_card_ind == len_deck:
                continue
            next_card_action = game_card_actions \
                .filter(CardAction.card_index == current_card_ind) \
                .first()
            next_card_action.player = players_mod[action.turn % num_players]
            current_card_ind += 1
    session.commit()
session.close()

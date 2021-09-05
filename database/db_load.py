import py.utils as u
from py.utils import logger
from database.db_connect import session, Game, Card, GameAction, PlayerNotes, Variant, CardAction, Clue, Player, Slot


def load_game(g, s):
    g_id = g['id']
    opt = s['options']
    try:
        starting_player = g['options']['startingPlayer']
    except KeyError:
        starting_player = opt['startingPlayer']
    game = Game(
        g_id,
        opt['numPlayers'],
        g['players'],
        starting_player,
        opt['variantID'],
        opt['variantName'],
        opt['timed'],
        opt['timeBase'],
        opt['timePerTurn'],
        opt['speedrun'],
        opt['cardCycle'],
        opt['deckPlays'],
        opt['emptyClues'],
        opt['oneExtraCard'],
        opt['oneLessCard'],
        opt['allOrNothing'],
        opt['detrimentalCharacters'],
        s['score'],
        s['numTurns'],
        s['endCondition'],
        s['datetimeStarted'],
        s['datetimeFinished'],
        s['numGamesOnThisSeed'],
        s['tags'],
        g['seed']
    )
    session.add(game)
    return game


def load_deck(g):
    deck = g['deck']
    seed = session.query(Card.seed) \
        .filter(Card.seed == g['seed'])\
        .first()
    if seed is not None:
        return
    for i in range(len(deck)):
        card = Card(
            g['seed'],
            i,
            deck[i]['suitIndex'],
            deck[i]['rank']
        )
        session.add(card)


def load_actions(g):
    g_id = g['id']
    actions = g['actions']
    for i in range(len(actions)):
        action = GameAction(
            g_id,
            i,
            actions[i]['type'],
            actions[i]['target'],
            actions[i]['value'],
        )
        session.add(action)


def load_notes(g):
    g_id = g['id']
    try:
        game_notes = g['notes']
        for i in range(len(game_notes)):
            player_notes = PlayerNotes(
                g_id,
                g['players'][i],
                game_notes[i]
            )
            session.add(player_notes)
    except KeyError:
        return


def update_game(s):
    g_id = s['id']
    opt = s['options']
    game = session.query(Game).filter(Game.game_id == g_id).first()
    if game is None:
        logger.info(f'{g_id} doesn\'t exist in db.')
        return -1
    num_players = session.query(Game.num_players).filter(Game.game_id == g_id).scalar()
    if num_players is not None:
        return 0
    game.num_players = opt['numPlayers']
    if game.starting_player is None:
        game.starting_player = opt['startingPlayer']
    game.variant_id = opt['variantID']
    game.variant = opt['variantName']
    game.timed = opt['timed']
    game.time_base = opt['timeBase']
    game.time_per_turn = opt['timePerTurn']
    game.speedrun = opt['speedrun']
    game.card_cycle = opt['cardCycle']
    game.deck_plays = opt['deckPlays']
    game.empty_clues = opt['emptyClues']
    game.one_extra_card = opt['oneExtraCard']
    game.one_less_card = opt['oneLessCard']
    game.all_or_nothing = opt['allOrNothing']
    game.detrimental_characters = opt['detrimentalCharacters']
    game.score = s['score']
    game.num_turns = s['numTurns']
    game.end_condition = s['endCondition']
    game.date_time_started = s['datetimeStarted']
    game.date_time_finished = s['datetimeFinished']
    game.num_games_on_this_seed = s['numGamesOnThisSeed']
    game.tags = s['tags']
    return 1


def load_variant(variant, variant_id):
    var = Variant(
        variant_id,
        variant,
        *[None] * 14
    )
    session.add(var)


def load_game_empty(g):
    g_id = g['id']
    try:
        starting_player = g['options']['startingPlayer']
    except KeyError:
        starting_player = None
    game = Game(
        g_id,
        None,
        g['players'],
        starting_player,
        *[None] * 20,
        g['seed']
    )
    session.add(game)


def init_piles(variant, suits):
    if 'Up or Down' in variant:
        piles = [[0, '']] * u.get_number_of_suits(variant)
    else:
        piles = [[0, 'up']] * u.get_number_of_suits(variant)
        if 'Reversed' in variant:
            piles[len(suits) - 1] = [6, 'down']
    return piles


def load_card_action_empty(deck, game_id, suits):
    for card in deck:
        new_card_action = CardAction(
            card.card_index,
            game_id,
            suits[card.suit_index],
            card.rank,
            *[None] * 4
        )
        session.add(new_card_action)


def init_hands(current_card_ind, players_orig, cards_per_hand, game_id):
    for i in range(current_card_ind):
        player = players_orig[i // cards_per_hand]
        card_action = session.query(CardAction)\
            .filter(CardAction.game_id == game_id)\
            .filter(CardAction.card_index == i)\
            .first()
        card_action.player = player
        card_action.turn_drawn = 0


def create_clue(action, colors, game_id, num_players, players_mod, players_orig):
    # color
    if action.action_type == 2:
        value = colors[action.value]
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


def init_action_type(action, suits, card_action, piles):
    if action.action_type == 0:
        card_suit_ind = suits.index(card_action.card_suit)
        if not u.is_played(piles, card_suit_ind, card_action.card_rank):
            card_action.action_type = 'misplay'
        else:
            card_action.action_type = 'play'
            piles[card_suit_ind] = [
                card_action.card_rank,
                u.up_or_down_direction(piles, card_suit_ind, card_action.card_rank)
            ]
    elif action.action_type == 1:
        card_action.action_type = 'discard'
    return card_action


def load_card_actions_and_clues(db_game):
    game_id = db_game.game_id
    seed = db_game.seed
    players_orig = db_game.players
    num_players = db_game.num_players
    variant_id = db_game.variant_id
    variant = db_game.variant
    starting_player = db_game.starting_player
    one_less_card = db_game.one_less_card
    one_extra_card = db_game.one_extra_card

    actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
    players_mod = (players_orig[starting_player:] + players_orig[:starting_player])

    suits, colors = session.query(Variant.suits, Variant.colors).filter(Variant.variant_id == variant_id).first()
    piles = init_piles(variant, suits)

    deck = session.query(Card).filter(Card.seed == seed).all()
    load_card_action_empty(deck, game_id, suits)

    current_card_ind = u.get_number_of_starting_cards(num_players, one_less_card, one_extra_card)
    cards_per_hand = u.get_number_of_cards_in_hand(num_players, one_less_card, one_extra_card)
    init_hands(current_card_ind, players_orig, cards_per_hand, game_id)

    card_actions = session.query(CardAction).filter(CardAction.game_id == game_id).all()

    for action in actions:
        if action.action_type == 4:
            return
        elif u.is_clued(action):
            create_clue(action, colors, game_id, num_players, players_mod, players_orig)
        elif action.action_type in [0, 1]:
            card_action = [c for c in card_actions if c.card_index == action.target][0]
            card_action = init_action_type(action, suits, card_action, piles)
            card_action.turn_action = action.turn + 1
            if current_card_ind == len(deck):
                continue
            next_card_action = [c for c in card_actions if c.card_index == current_card_ind][0]
            next_card_action.turn_drawn = action.turn + 1
            next_card_action.player = players_mod[action.turn % num_players]
            current_card_ind += 1


def update_action_types(db_game):
    game_id, variant = db_game.game_id, db_game.variant
    actions = session.query(GameAction).filter(GameAction.game_id == game_id).all()
    suits = session.query(Variant.suits).filter(Variant.variant == variant).scalar()
    piles = init_piles(variant, suits)
    card_actions = session.query(CardAction).filter(CardAction.game_id == game_id).all()

    for action in actions:
        if action.action_type in [0, 1]:
            card_action = [c for c in card_actions if c.card_index == action.target][0]
            init_action_type(action, suits, card_action, piles)


def load_player(player):
    session.add(Player(player))


def load_slots(card_action, turn, slot):
    movement = Slot(
        card_action.game_id,
        card_action.card_index,
        turn,
        slot)
    session.add(movement)

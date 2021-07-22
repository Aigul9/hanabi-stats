import logging

from database.db_connect import session, Game, Card, GameAction, PlayerNotes, Variant


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
        None,
        None,
        None,
        None,
        None,
        None
    )
    session.add(var)


def load_empty_game(g):
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
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        g['seed']
    )
    session.add(game)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

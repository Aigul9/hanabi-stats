from database.db_schema import Game, Card, GameAction, PlayerNotes
from database.db_connect import session


def load_game(g):
    g_id = g['id']
    try:
        opt = g['options']
        try:
            var = opt['variant']
        except KeyError:
            var = None
        try:
            speedrun = opt['speedrun']
        except KeyError:
            speedrun = None
    except KeyError:
        var = None
        speedrun = None
    game = Game(
        g_id,
        g['players'],
        var,
        speedrun,
        g['seed']
    )
    session.add(game)


def load_deck(g):
    deck = g['deck']
    for i in range(len(deck)):
        db_card = session.query(Card) \
            .filter(Card.seed == g['seed']) \
            .filter(Card.card_index == i) \
            .scalar()
        if db_card is None:
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
        pass

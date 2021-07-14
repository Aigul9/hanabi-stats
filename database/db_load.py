from database.db_schema import Game, GameAction, PlayerNotes
from database.db_connect import session


def load(g_id, g):
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
    actions = g['actions']
    game = Game(
        g_id,
        g['players'],
        var,
        speedrun,
        g['seed']
    )
    for i in range(len(actions)):
        action = GameAction(
            g_id,
            i,
            actions[i]['type'],
            actions[i]['target'],
            actions[i]['value'],
        )
        session.add(action)
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
    session.add(game)

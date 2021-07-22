import py.utils as u
from database.db_connect import session, Game, Card, GameAction, PlayerNotes


# TODO: refactor using only db
def get_notes_rate(user, stats):
    stats = u.filter_id_notes(u.clear_2p(stats))
    stats = stats[:len(stats) - 10]
    user_rate = {'pl_notes': 0, 'visible_cards': 0}
    for s in stats:
        g_id = s['id']
        actions = session.query(GameAction).filter(GameAction.game_id == g_id).all()
        players = session.query(Game.players).filter(Game.game_id == g_id).scalar()
        deck = session.query(Card).filter(Card.seed == s['seed']).all()
        total_cards = len(deck)
        try:
            starting_cards = u.get_number_of_starting_cards(
                len(players),
                s['options']['oneLessCard'],
                s['options']['oneExtraCard']
            )
        except TypeError:
            continue
        drawn_cards = u.get_number_of_plays_or_discards(actions)
        visible_cards = min(starting_cards + drawn_cards, total_cards)
        pl_notes = session.query(PlayerNotes.notes) \
            .filter(PlayerNotes.game_id == g_id) \
            .filter(PlayerNotes.player == user) \
            .scalar()
        if pl_notes is not None:
            pl_notes = len([r for r in pl_notes if r != ''])
        else:
            continue
        user_rate['pl_notes'] += pl_notes
        user_rate['visible_cards'] += visible_cards
    return round(user_rate['pl_notes'] / user_rate['visible_cards'], 4)

import py.utils as ut
from database.db_connect import session
from database.db_schema import Game, Card, GameAction, PlayerNotes

users = ut.open_file('../input/list_of_players_notes.txt')

users_rates = {}
for u in users:
    print(u)
    start = ut.current_time()
    print('Start time:', start)
    # 103000 - starting id for notes
    stats = ut.filter_by_id(ut.clear_speedruns(ut.clear_2p(ut.open_stats(u))), [103000])
    stats = stats[:len(stats) - 10]
    u_rate = {'pl_notes': 0, 'visible_cards': 0}
    for s in stats:
        g_id = s['id']
        actions = session.query(GameAction).filter(GameAction.game_id == g_id).all()
        players = session.query(Game.players).filter(Game.game_id == g_id).scalar()
        deck = session.query(Card).filter(Card.seed == s['seed']).all()
        total_cards = len(deck)
        try:
            starting_cards = ut.get_number_of_starting_cards(len(players))
        except TypeError:
            continue
        drawn_cards = ut.get_number_of_plays_or_discards(actions)
        visible_cards = min(starting_cards + drawn_cards, total_cards)
        pl_notes = session.query(PlayerNotes.notes) \
            .filter(PlayerNotes.game_id == g_id) \
            .filter(PlayerNotes.player == u) \
            .scalar()
        if pl_notes is not None:
            pl_notes = len([r for r in pl_notes if r != ''])
        else:
            continue
        u_rate['pl_notes'] += pl_notes
        u_rate['visible_cards'] += visible_cards
        # print(f"{g_id}\t{pl_notes}\t{visible_cards}\t{pl_notes / visible_cards}")
    users_rates[u] = u_rate
    print('rate', u_rate['pl_notes'], u_rate['visible_cards'])
    print(u_rate['pl_notes'] / u_rate['visible_cards'])
    print('End time:', ut.current_time())
    # ut.time_spent(start)
    ut.save(f'notes_rate', {u: round(u_rate['pl_notes'] / u_rate['visible_cards'], 4)}, ['Player', 'Rate'])

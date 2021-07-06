import py.util as ut

with open('../input/list_of_players_test.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

users_rates = {}
for u in users:
    print(u)
    start = ut.current_time()
    print('Start time:', start)
    # 103000 - starting id for notes
    stats = ut.filter_by_id(ut.clear_speedruns(ut.clear_2p(ut.open_stats(u))), [103000])
    u_rate = {'pl_notes': 0, 'visible_cards': 0}
    for s in stats:
        g_id = s['id']
        game = ut.export_game(g_id)
        actions = game['actions']
        players = game['players']
        total_cards = len(game['deck'])
        starting_cards = ut.get_number_of_starting_cards(len(players))
        drawn_cards = ut.get_number_of_plays_or_discards(actions)
        visible_cards = min(starting_cards + drawn_cards, total_cards)
        try:
            notes = game['notes']
            pl_notes = notes[ut.get_player_index(game, u)]
            pl_notes = len([r for r in pl_notes if r != ''])
        except KeyError:
            pl_notes = 0
        u_rate['pl_notes'] += pl_notes
        u_rate['visible_cards'] += visible_cards
        # print(f"{g_id}\t{pl_notes}\t{visible_cards}\t{pl_notes / visible_cards}")
    users_rates[u] = u_rate
    print('rate', u_rate['pl_notes'], u_rate['visible_cards'])
    print(u_rate['pl_notes'] / u_rate['visible_cards'])
    print('End time:', ut.current_time())
    # ut.time_spent(start)
    ut.save(f'notes_rate', {u: round(u_rate['pl_notes'] / u_rate['visible_cards'], 4)}, ['Player', 'Rate'])

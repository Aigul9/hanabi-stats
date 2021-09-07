import py.utils as ut


def variation(start, val):
    if val - start >= 0:
        return val - start
    else:
        return val - start + len(indices)


username = 'Valetta6789'
indices = [0, 1, 2]
data = ut.get_3p(ut.open_stats(username))
data = ut.contains_user(data, 'florrat2')
data = ut.contains_user(data, 'Libster')
data = ut.filter_by_id(data, [558639, 558730])
cards_clued = {
    # 'r3': {
    #     'suitIndex': 0,
    #     'rank': 3
    # },
    # 'y3': {
    #     'suitIndex': 1,
    #     'rank': 3
    # },
    # 'g3': {
    #     'suitIndex': 2,
    #     'rank': 3
    # },
    # 'b3': {
    #     'suitIndex': 3,
    #     'rank': 3
    # },
    # 'p3': {
    #     'suitIndex': 4,
    #     'rank': 3
    # },
    # 'r4': {
    #     'suitIndex': 0,
    #     'rank': 4
    # },
    # 'y4': {
    #     'suitIndex': 1,
    #     'rank': 4
    # },
    # 'g4': {
    #     'suitIndex': 2,
    #     'rank': 4
    # },
    # 'b4': {
    #     'suitIndex': 3,
    #     'rank': 4
    # },
    # 'p4': {
    #     'suitIndex': 4,
    #     'rank': 4
    # }
    'r2': {
            'suitIndex': 0,
            'rank': 2
    }
}
cards_played = {
    # 'r4': {
    #     'suitIndex': 0,
    #     'rank': 4
    # },
    'y4': {
        'suitIndex': 1,
        'rank': 4
    },
    'g4': {
        'suitIndex': 2,
        'rank': 4
    },
    # 'b4': {
    #     'suitIndex': 3,
    #     'rank': 4
    # },
    'p4': {
        'suitIndex': 4,
        'rank': 4
    },
    # 'r5': {
    #     'suitIndex': 0,
    #     'rank': 5
    # },
    'y5': {
        'suitIndex': 1,
        'rank': 5
    },
    'g5': {
        'suitIndex': 2,
        'rank': 5
    },
    # 'b5': {
    #     'suitIndex': 3,
    #     'rank': 5
    # },
    'p5': {
        'suitIndex': 4,
        'rank': 5
    }
}
results = []
for r in data:
    ex = ut.export_game(r)
    # print(ex['id'])
    val_index = ut.get_player_index(ex, username)
    action_val = {
        # "type": 2,
        "type": 2,
        "target": ut.switch_rank_mod_next(val_index),
        # "value": 0
        # "value": 4
        "value": 0
    }
    # action_val_2 = {
    #     "type": 2,
    #     "target": switch_rank_mod(val_index),
    #     "value": 5
    # }
    for i in range(1):
        # try:
        #     # card_index_fire = get_card_index(ex, cards_clued[list(cards_clued.keys())[i]])
        #     # card_index_after_fire = get_card_index(ex, cards_played[list(cards_played.keys())[i]])
        # except ValueError:
        #     continue
        # action_fire = {
        #     "type": 0,
        #     "target": card_index_fire,
        #     "value": 0
        # }
        # action_after_fire = {
        #     "type": 0,
        #     "target": card_index_after_fire,
        #     "value": 0
        # }
        actions = ex['actions']
        for j in range(2, len(actions)):
            if actions[j-2] == action_val:
                # and actions[j-1] == action_fire:
                # or actions[j-2] == action_val_2)\
                # and actions[j] == action_after_fire:
                # and j-1 % 3 == variation(start_index, val_index):
                results.append([ex['id'], actions[j], j])
                print('result:', actions[j], f'hanab.live/replay/{ex["id"]}#{j}')

print('=====')
print(results)

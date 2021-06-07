import requests


def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


def get_3p(stats):
    return [row for row in stats if int(row['options']['numPlayers']) == 3]


def contains_user(stats, user):
    return [row for row in stats if user in row['playerNames']]


def export_game(game):
    url = f'https://hanab.live/export/{game["id"]}'
    response = requests.get(url)
    return response.json()


def get_player_index(export, player):
    return export['players'].index(player)


def switch_rank_mod(index):
    return indices[(index + 2) % len(indices)]


def get_card_index(export, card):
    return export['deck'].index(card)


def variation(start, val):
    if val - start >= 0:
        return val - start
    else:
        return val - start + len(indices)


username = 'Valetta6789'
indices = [0, 1, 2]
data = get_3p(open_stats(username))
cards_clued = {
    # 'r3': {
    #     'suitIndex': 0,
    #     'rank': 3
    # },
    'y3': {
        'suitIndex': 1,
        'rank': 3
    },
    'g3': {
        'suitIndex': 2,
        'rank': 3
    },
    # 'b3': {
    #     'suitIndex': 3,
    #     'rank': 3
    # },
    'p3': {
        'suitIndex': 4,
        'rank': 3
    },
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
    ex = export_game(r)
    # print(ex['id'])
    val_index = get_player_index(ex, username)
    action_val = {
        # "type": 2,
        "type": 2,
        "target": switch_rank_mod(val_index),
        # "value": 0
        # "value": 4
        "value": 4
    }
    action_val_2 = {
        "type": 2,
        "target": switch_rank_mod(val_index),
        "value": 5
    }
    for i in range(4):
        try:
            card_index_fire = get_card_index(ex, cards_clued[list(cards_clued.keys())[i]])
            card_index_after_fire = get_card_index(ex, cards_played[list(cards_played.keys())[i]])
        except ValueError:
            continue
        action_fire = {
            "type": 0,
            "target": card_index_fire,
            "value": 0
        }
        action_after_fire = {
            "type": 0,
            "target": card_index_after_fire,
            "value": 0
        }
        actions = ex['actions']
        for j in range(2, len(actions)):
            if (actions[j-2] == action_val or actions[j-2] == action_val_2)\
                    and actions[j-1] == action_fire:
                    # and actions[j] == action_after_fire:
                    # and j-1 % 3 == variation(start_index, val_index):
                results.append([ex['id'], actions[j], j])
                print('result:', ex['id'], actions[j], j)

print('=====')
print(results)

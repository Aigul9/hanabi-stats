import requests
import csv


def export_game(game_id):
    url = f'https://hanab.live/export/{game_id}'
    response = requests.get(url)
    return response.json()


def load_games():
    with open(f'../input/games_compare.txt', 'r', encoding='utf-8') as f:
        games_1 = []
        games_2 = []
        for line in f.readlines():
            games = line.strip().split(';')
            games_1.append(games[0])
            games_2.append(games[1])
    return games_1, games_2


def convert_action_types(action_type):
    action_types = ['play', 'discard', 'color', 'rank']
    return action_types[action_type]


def get_action_type_length(actions, action_type):
    return len([a for a in actions if a['type'] == action_type])


def generate_stats(ids):
    stats = {}
    action_types = [0, 1, 2, 3]
    for i in ids:
        game = export_game(i)
        actions = game['actions']
        seed = game['seed']
        stats[seed] = {}
        stats[seed]['team'] = game['players']
        stats[seed]['game_id'] = game['id']
        stats[seed]['turns'] = len(actions)
        for t in action_types:
            stats[seed][t] = get_action_type_length(actions, t)
    return stats


def combine_dict(stats):
    combined_stats = {}
    for k in stats[0].keys():
        combined_stats[k] = []
        for i in range(len(stats)):
            combined_stats[k].append(stats[i][k])
    return combined_stats


def save(all_stats):
    with open(f'../output/comp_comparison.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['Team', 'Game id', 'Turns', 'Play', 'Discard', 'Color clue', 'Rank clue', 'Seed'])
        for k in all_stats[0].keys():
            for i in range(len(all_stats)):
                stats_list = all_stats[i][k]
                stats_list['team'] = ', '.join(stats_list['team'])
                stats_list = list(stats_list.values())
                stats_list.append(k)
                w.writerow(stats_list)


lib_games, val_games = load_games()
lib_stats = generate_stats(lib_games)
val_stats = generate_stats(val_games)
# print(lib_stats)
save([lib_stats, val_stats])


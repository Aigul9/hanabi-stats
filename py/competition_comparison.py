import csv
import py.utils as u


def load_games():
    with open(f'../input/games_compare.txt', 'r', encoding='utf-8') as f:
        games_1 = []
        games_2 = []
        for line in f.readlines():
            games = line.strip().split(';')
            games_1.append(games[0])
            games_2.append(games[1])
    return games_1, games_2


def generate_stats(ids):
    stats = {}
    action_types = [0, 1, 2, 3]
    for i in ids:
        game = u.export_game(i)
        actions = game['actions']
        seed = game['seed']
        stats[seed] = {}
        stats[seed]['team'] = game['players']
        stats[seed]['game_id'] = game['id']
        stats[seed]['turns'] = len(actions)
        for t in action_types:
            stats[seed][t] = u.get_action_type_length(actions, t)
    return stats


def update_clue(seed):
    seed[2] = seed[2] + seed[3]
    del seed[3]
    return seed


def join_teams(teams):
    return ', '.join(teams)


def id_to_link(game_id):
    return f'hanab.live/replay/{game_id}'


def combine_dict(stats):
    combined_stats = {}
    for seed in stats[0].keys():
        combined_stats[seed] = {}
        for k in stats[0][seed].keys():
            combined_part = []
            # number of lists that needs to be combined
            for i in range(len(stats)):
                combined_part.append(stats[i][seed][k])
            combined_stats[seed][k] = combined_part
    return combined_stats


def save_row(all_stats):
    with open(f'../output/comp_comparison_row.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['Team', 'Game id', 'Turns', 'Play', 'Discard', 'Clue', 'Seed'])
        for k in all_stats[0].keys():
            for s in all_stats:
                stats_list = s[k]
                stats_list['team'] = join_teams(stats_list['team'])
                stats_list['game_id'] = id_to_link(stats_list['game_id'])
                stats_list = update_clue(stats_list)
                stats_list = list(stats_list.values())
                stats_list.append(k)
                w.writerow(stats_list)


def save_column(combined_stats):
    with open(f'../output/comp_comparison_col.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        header = []
        for i in range(1, len(list(combined_stats.values())[0]['team']) + 1):
            header.append(f'Team {str(i)}')
        w.writerow(['Column', *header])
        for k, v in combined_stats.items():
            teams = []
            for team in v['team']:
                teams.append(join_teams(team))
            w.writerow(['Team', *teams])
            w.writerow(['Seed', k, k])
            links = []
            for game_id in v['game_id']:
                links.append(id_to_link(game_id))
            w.writerow(['Link', *links])
            w.writerow(['Turns', *v['turns']])
            w.writerow(['Play', *v[0]])
            w.writerow(['Discard', *v[1]])
            clues = [[*v[2]], [*v[3]]]
            w.writerow(['Clue', *[sum(c) for c in zip(*clues)]])


lib_games, val_games = load_games()
lib_stats = generate_stats(lib_games)
val_stats = generate_stats(val_games)
# save_row([lib_stats, val_stats])
save_column(combine_dict([lib_stats, val_stats]))

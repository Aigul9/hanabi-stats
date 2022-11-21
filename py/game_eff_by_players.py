from collections import defaultdict

import py.utils as u

if __name__ == '__main__':
    current_eff_dict = defaultdict(float)
    num_games_dict = defaultdict(int)
    HPLAYERS = u.open_file('../input/players.txt')

    with open('../output/requests/current_eff_by_teams.tsv', 'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            players, eff, _, _ = line.split('\t')
            players = players.split(', ')
            # print(players)
            for p in players:
                if p not in HPLAYERS:
                    continue
                current_eff_dict[p] += float(eff)
                num_games_dict[p] += 1
    print(current_eff_dict, num_games_dict)
    res = {k: [round(current_eff_dict[k] / num_games_dict[k], 2), num_games_dict[k]] for k in current_eff_dict.keys()}
    sorted_res = dict(sorted(res.items(), key=lambda item: (-item[1][0], item[0])))
    path = '../output/requests/current_eff_by_player'
    u.save(path, sorted_res, ['Player', 'Avg eff', 'Num of games'])

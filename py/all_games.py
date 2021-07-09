import py.utils as ut
import csv


with open('../input/list_of_players_notes.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


games = []
for u in users:
    print(u)
    stats = ut.filter_non_bga(ut.clear_speedruns(ut.clear_2p(ut.open_stats(u))))
    for s in stats:
        game_id = s['id']
        if game_id not in games:
            starting_player_ind = s['options']['startingPlayer']
            variant = s['options']['variantName']
            game = {'id': game_id, 'spi': starting_player_ind, 'result': 'loss'}
            if s['score'] == ut.get_max_score(variant):
                game['result'] = 'win'
            games.append(game)

# print(games)
with open(f'../output/misc/all_games.tsv', 'w', encoding='utf-8', newline='') as file:
    w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
    for g in games:
        w.writerow([g['id'], g['spi'], g['result']])

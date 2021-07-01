import requests
import logging
import csv
from py.HQL.UserStats import UserStats


def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


def open_game(game_id):
    url = f'https://hanab.live/export/{game_id}'
    response = requests.get(url)
    return response.json()

# def apply_model(response):
#     return [UserStats(*game_json.values()) for game_json in response]


def filter_equal(array, field, condition, options):
    try:
        if options:
            return [row for row in array if row['options'][field] == condition]
        return [row for row in array if row[field] == condition]
    except KeyError:
        logging.error(f'Incorrect field name.')
        return array


def filter_contains(array, field, condition, options):
    try:
        if options:
            return [row for row in array if condition in row['options'][field]]
        return [row for row in array if condition in row[field]]
    except KeyError:
        logging.error(f'Incorrect field name: {field}.')
        return array


def save(data):
    with open(f'../../output/misc/HQL.txt', 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')


if __name__ == "__main__":
    from py.HQL.HQL_test import username, query

    print('start')

    with open('../../input/list_of_players.txt', 'r') as f:
        users = [line.rstrip() for line in f.readlines()]

    # with open(f'../../output/misc/just_results.tsv', 'w', newline='') as f:
    #     w = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     w.writerow(['test'])
    # for u in users:
    #     print(f'Current user: {u}')
        # stats = apply_model(open_stats(username))
    stats = open_stats(username)
    filtered = stats
    for q in query.items():
        if q[0] == 'options':
            for k in query[q[0]].items():
                filtered = filter_equal(filtered, *k, True)
                # filtered = filter_contains(filtered, *k, True)
        else:
            # filtered = filter_contains(filtered, *q, False)
            filtered = filter_equal(filtered, *q, False)
    # print(len(filtered))
    # save(filtered)

    count = 1
    for g in filtered:
        g_id = g['id']
        game = open_game(g_id)
        # print(f'Step {count}: {g_id}')
        count += 1
        try:
            notes = game['notes']
            for i in range(len(notes)):
                for n1 in notes[i]:
                    # if '\u0026gt' in n1 and '-\u0026gt' not in n1 and '\u0026gt;\u0026lt' not in n1:
                    if 'nocm' in n1:
                        # w.writerow([g_id, game['players'], game['players'][i], n1])
                        print(f"{g_id}\t{game['players']}\t{game['players'][i]}\t{n1}")
        except KeyError:
            break
            # pass
            # print('end', g_id)
            # exit()

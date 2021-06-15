import requests
import logging
import csv
from py.HQL.UserStats import UserStats


def open_stats(user):
    url = f'https://hanab.live/history/{user}?api'
    response = requests.get(url)
    return response.json()


# def apply_model(response):
#     return [UserStats(*game_json.values()) for game_json in response]


def filter_equal(field, condition, options):
    try:
        if options:
            return [row for row in stats if row['options'][field] == condition]
        return [row for row in stats if row[field] == condition]
    except KeyError:
        logging.error(f'Incorrect field name.')
        return stats


def filter_contains(array, field, condition, options):
    try:
        if options:
            return [row for row in array if condition in row['options'][field]]
        return [row for row in array if condition in row[field]]
    except KeyError:
        logging.error(f'Incorrect field name: {field}.')
        return array


def save(data):
    with open(f'../../output/misc/HQL.txt', 'w') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')


if __name__ == "__main__":
    from py.HQL.HQL_test import username, query
    # stats = apply_model(open_stats(username))
    stats = open_stats(username)
    filtered = stats
    for q in query.items():
        if q[0] == 'options':
            for k in query[q[0]].items():
                filtered = filter_contains(filtered, *k, True)
        else:
            filtered = filter_contains(filtered, *q, False)
            # filtered = filter_equal(*q, False)
    print(len(filtered))
    save(filtered)

import errno

import requests
from bs4 import BeautifulSoup
import os


def get_number_of_suits(variant):
    default_suits = {
        '3 Suits': 3,
        '4 Suits': 4,
        'No Variant': 5,
        '6 Suits': 6,
        'Dual-Color Mix': 6,
        'Ambiguous Mix': 6,
        'Ambiguous & Dual-Color': 6
    }
    return default_suits.get(variant, variant[-8:-7])


def get_history_table(username):
    url = 'https://hanab.live/history/' + username
    try:
        page = requests.get(url)
    except:
        print('Check your internet connection.')
        exit()
    if page.status_code != 200:
        print('Username is not valid:', username)
        exit()
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find(id='history-table')


def get_stats(history_table):
    items = []
    for tr in history_table.findAll('tr')[1:]:
        item = []
        for td in tr.findAll('td'):
            item.append(td.text.replace('\n', '').strip())
        suits = get_number_of_suits(item[3])
        items.append([*item, suits, int(suits) * 5])
    return items


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def save_stats(items, username):
    path = f'../temp/{username}_stats.txt'
    mkdir_p(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            file_item = ''
            for i in item:
                file_item += '{}\t'.format(i)
            f.write('{}\n'.format(file_item.rstrip()))


def save_list_of_players(items, username):
    path = f'../temp/{username}_players.txt'
    mkdir_p(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write('{}\n'.format(item[5]))

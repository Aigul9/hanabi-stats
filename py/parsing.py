import requests
from bs4 import BeautifulSoup
from py.constants import username


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


URL = 'https://hanab.live/history/' + username
page = requests.get(URL)
if page.status_code != 200:
    print('Username is not valid.')
    exit()

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='history-table')
items = []

for tr in results.findAll('tr')[1:]:
    item = []
    for td in tr.findAll('td'):
        item.append(td.text.replace('\n', '').strip())
    suits = get_number_of_suits(item[3])
    items.append([*item, suits, int(suits) * 5])

with open(f'../user_files/{username}_stat.txt', 'w', encoding='utf-8') as f:
    for item in items:
        file_item = ''
        for i in item:
            file_item += '{}\t'.format(i)
        f.write('{}\n'.format(file_item.rstrip()))

with open(f'../user_files/{username}_players.txt', 'w', encoding='utf-8') as f:
    for item in items:
        f.write('{}\n'.format(item[5]))

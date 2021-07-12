import csv
import requests
from bs4 import BeautifulSoup
import py.utils as ut


def get_content(url, username):
    page = requests.get(url)
    if page.status_code != 200:
        print('Username is not valid:', username)
        exit()
    return BeautifulSoup(page.content, 'html.parser')


def get_digits(text):
    return int(text.split()[0].replace('<td>', ''))


def get_total_scores(username):
    url = 'https://hanab.live/missing-scores/' + username
    soup = get_content(url, username)
    text = soup.find_all('td')
    return [get_digits(str(t)) for t in text]


users = ut.open_file('../input/list_of_players_notes.txt')
scores = {}
for u in users:
    scores[u] = get_total_scores(u)
scores = {k: v for k, v in sorted(scores.items(), key=lambda i: -i[1][5])}
ut.save('total_max_scores', scores, ['Player', '2p', '3p', '4p', '5p', '6p', 'Total scores'])

import requests
from bs4 import BeautifulSoup


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

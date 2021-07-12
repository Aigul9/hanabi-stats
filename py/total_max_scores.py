import requests
from bs4 import BeautifulSoup


def get_history_table(username):
    url = 'https://hanab.live/scores/' + username
    page = requests.get(url)
    if page.status_code != 200:
        print('Username is not valid:', username)
        exit()
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    # return soup.find(id='history-table')

get_history_table('Valetta6789')
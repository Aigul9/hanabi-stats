import requests
from bs4 import BeautifulSoup

import py.utils as u
from database.db_connect import session, Player


def get_content(url, username, req_session=None):
    """Parses content from the html page.

    Parameters
    ----------
    url : str
        URL
    username : str
        Player name
    req_session
        Session

    Returns page content.
    """
    if session is None:
        page = requests.get(url)
    else:
        page = req_session.get(url)
    if page.status_code != 200:
        print('Username is not valid:', username)
        exit()
    return BeautifulSoup(page.content, 'html.parser')


def get_digits(text):
    """Gets digits from the provided string.

    Parameters
    ----------
    text : str
        Text containing html tags

    Returns digits.
    """
    return int(text.split()[0].replace('<td>', ''))


def get_total_scores(username, req_session):
    """Gets number of achieved scores from the user's personal page.

    Parameters
    ----------
    username : str
        Player name
    req_session
        Session

    Returns number of scores.
    """
    url = 'https://hanab.live/missing-scores/' + username
    soup = get_content(url, username, req_session)
    text = soup.find_all('td')
    return [get_digits(str(t)) for t in text]


if __name__ == "__main__":
    users = session.query(Player.player).all()
    request_session = requests.Session()
    scores = {}
    for user in users:
        user = user[0]
        scores[user] = get_total_scores(user, request_session)
    print(scores)
    u.save(
        '../output/scores/total_max_scores',
        u.sort(scores, 5),
        ['Player', '2p', '3p', '4p', '5p', '6p', 'Total scores']
    )

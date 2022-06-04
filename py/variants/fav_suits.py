import csv
from sqlalchemy import false

from database.db_connect import session, Game, Player


def save_all():
    """Saves all suits with number of games for each player."""
    with open('../../output/variants/favourite_suits.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player',
                    'Rainbow',
                    'Prism',
                    'White',
                    'Black',
                    'Pink',
                    'Light Pink',
                    'Brown',
                    'Muddy Rainbow',
                    'Omni',
                    'Null',
                    'Dark Rainbow',
                    'Dark Prism',
                    'Gray',
                    'Dark Pink',
                    'Gray Pink',
                    'Dark Brown',
                    'Cocoa Rainbow',
                    'Dark Omni',
                    'Dark Null'])
        for k, v in sorted(players_suits.items(), key=lambda x: x[0].lower()):
            w.writerow([
                k,
                v['Rainbow'],
                v['Prism'],
                v['White'],
                v['Black'],
                v['Pink'],
                v['Light Pink'],
                v['Brown'],
                v['Muddy Rainbow'],
                v['Omni'],
                v['Null'],
                v['Dark Rainbow'],
                v['Dark Prism'],
                v['Gray'],
                v['Dark Pink'],
                v['Gray Pink'],
                v['Dark Brown'],
                v['Cocoa Rainbow'],
                v['Dark Omni'],
                v['Dark Null']
            ])


def save_top():
    """Saves top 5 suits with number of games for each player."""
    with open('../../output/variants/favourite_suits_top_r.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player',
                    'Suit #1', 'Count #1',
                    'Suit #2', 'Count #2',
                    'Suit #3', 'Count #3',
                    'Suit #4', 'Count #4',
                    'Suit #5', 'Count #5'])
        for k, v in sorted(players_suits.items(), key=lambda x: x[0].lower()):
            total = sum(v.values())
            v = {k1: round(v1 / total * 100) for k1, v1 in v.items()}
            v = sorted(v.items(), key=lambda x: -x[1])
            w.writerow([
                k,
                v[0][0], f'{v[0][1]}%',
                v[1][0], f'{v[1][1]}%',
                v[2][0], f'{v[2][1]}%',
                v[3][0], f'{v[3][1]}%',
                v[4][0], f'{v[4][1]}%'
            ])


def clean_variant(variant):
    """Removes unnecessary text from the variant name.

    Parameters
    ----------
    variant : str

    Returns
    -------
    str
        Variant name without unused substrings and spaces
    """
    return variant\
        .replace('(3 Suits)', '')\
        .replace('(4 Suits)', '')\
        .replace('(5 Suits)', '')\
        .replace('(6 Suits)', '')\
        .replace('Reversed', '')\
        .strip()


def init_suits():
    """Initialises dictionary of suits.

    Returns
    -------
    dict
        Suits with 0 number of games
    """
    return {
        'White': 0,
        'Muddy Rainbow': 0,
        'Light Pink': 0,
        'Null': 0,
        'Rainbow': 0,
        'Pink': 0,
        'Brown': 0,
        'Omni': 0,
        'Prism': 0,
        'Dark Null': 0,
        'Dark Prism': 0,
        'Dark Rainbow': 0,
        'Dark Pink': 0,
        'Dark Brown': 0,
        'Dark Omni': 0,
        'Cocoa Rainbow': 0,
        'Gray Pink': 0,
        'Black': 0,
        'Gray': 0
    }


def get_variants(username):
    """Gets list of variant from the db for a specified player, excluding 2-player games and speedruns.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    list
        Player's games without 2-player and speedruns
    """
    return session.query(Game.variant) \
        .filter(Game.players.any(username)) \
        .filter(Game.num_players != 2) \
        .filter(Game.speedrun == false()) \
        .all()


def get_suits(username):
    """Calculates number of games containing a special suit.

    Parameters
    ----------
    username : str
        Player name

    Returns
    -------
    suits : dict
        Suits with calculated number of games
    """
    suits = init_suits()
    variants = get_variants(username)

    for var in variants:
        variant = var[0].split('&')
        variant = [clean_variant(v) for v in variant]
        for suit in variant:
            if suit in suits:
                suits[suit] += 1
    return suits


if __name__ == "__main__":
    users = session.query(Player.player).all()
    players_suits = {}
    for user in users:
        user = user[0]
        players_suits[user] = get_suits(user)

    save_all()
    save_top()

import pandas as pd
from collections import defaultdict
from sqlalchemy import func, false

from database.db_connect import session, Game, Card
import py.utils as u


if __name__ == '__main__':
    # query = """
    #     select seed from
    #     (select
    #         seed,
    #         count(game_id) filter(where score = 25) as num_max_scores,
    #         count(game_id) filter(where score < 25) as num_not_max_scores
    #     from games
    #     where seed like 'p4v0%%'
    #       and seed not like '%%old'
    #     group by seed) t
    #     where num_max_scores >= 50
    #     and num_not_max_scores >= 50
    #     limit 1
    # """

    suits_dict = {
        0: 'r',
        1: 'y',
        2: 'g',
        3: 'b',
        4: 'p'
    }

    games_with_max_score = (
        session
        .query(Game.game_id, Game.seed, Game.score)
        .filter(
            Game.seed.like('p4v0%'),
            Game.seed.notlike('%old'),
            Game.score == 25
        )
        .order_by(Game.game_id.desc())
        .limit(50)
        .all()
    )

    games_wo_max_score = (
        session
        .query(Game.game_id, Game.seed, Game.score)
        .filter(
            Game.seed.like('p4v0%'),
            Game.seed.notlike('%old'),
            Game.score < 25
        )
        .order_by(Game.game_id.desc())
        .limit(50)
        .all()
    )

    games = games_with_max_score + games_wo_max_score
    seeds = [row[1] for row in games]
    print(seeds)

    decks = (
        session
        .query(Card)
        .filter(Card.seed.in_(seeds))
        .all()
    )

    for game in games:
        game_id, seed, score = game
        deck = [d for d in decks if d.seed == seed][-10:]
        formula = 0
        for i in range(10):
            if i >= 5:
                formula += deck[i].rank * (i - 4)
            else:
                formula += deck[i].rank
        cards = [suits_dict.get(c.suit_index) + str(c.rank) for c in deck]
        print(game_id, seed, score, formula, cards, sep='\t')

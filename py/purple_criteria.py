from sqlalchemy import func, false, extract

from database.db_connect import session, Game

if __name__ == "__main__":
    players = session.query(func.unnest(Game.players), func.count(Game.game_id)) \
        .distinct() \
        .group_by(func.unnest(Game.players)) \
        .having(func.count(Game.game_id) >= 240) \
        .all()

    results = {}

    for p in players:
        p = p[0]
        grouped_games = session \
            .query(extract('year', Game.date_time_started),
                   extract('month', Game.date_time_started),
                   func.count(Game.game_id)) \
            .filter(Game.num_players != 2) \
            .filter(Game.speedrun == false()) \
            .filter(Game.players.any(p)) \
            .group_by(extract('year', Game.date_time_started),
                      extract('month', Game.date_time_started)) \
            .having(func.count(Game.game_id) >= 20) \
            .all()
        len_games = len(grouped_games)
        if len_games >= 12:
            results[p] = grouped_games
            print('======', p, '-----', len_games)

    print(sorted(results.keys()))

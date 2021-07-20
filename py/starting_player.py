import py.utils as u
from database.db_connect import session, Game


def get_alice_wr(user, stats):
    group = session.query(Game)\
        .filter(Game.players[Game.starting_player + 1] == user)\
        .filter(Game.num_players != 2)\
        .filter(Game.speedrun == 'false')\
        .all()
    stats = u.clear_2p(stats)
    # num games overall
    s_len = len(stats)
    # num wins overall
    total_wins = u.get_wins(stats)
    # num games going first
    g_len = len(group)
    # num wins going first
    group_wins = 0
    for g in group:
        if g.score == u.get_max_score(g.variant):
            group_wins += 1
    # num game not going first
    b_len = s_len - g_len
    # num wins not going first
    bob_wins = total_wins - group_wins
    formula = round((group_wins / g_len) / (bob_wins / b_len), 2)
    return formula, group_wins, g_len, bob_wins, b_len

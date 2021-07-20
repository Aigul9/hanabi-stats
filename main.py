import logging

import py.calc as c
import py.end_condition as e
import py.notes_portrait as np
import py.notes_portrait_afterwards as npa
import py.notes_rate as nr
import py.players as pls
import py.players_most_wl as wl
import py.starting_player as st
import py.time_spent as time
import py.total_max_scores as t
import py.utils as u


def main_user(user):
    global global_ranking, global_pref, global_teams
    logger.info(user)
    start_time = u.current_time()
    logger.info(start_time)
    # Get user's stats via api
    user_stats = u.clear_speedruns(u.open_stats(user))
    # Step 1: number of wins and losses in 2p/3p+ for 4 types of variants: easy, null, sd, dd
    up_to_date_stats[user] = c.get_all_stats(user_stats)
    players_list = pls.get_players_set(user_stats, user)
    # Step 2: stats above but for separated by players
    # wl.save_players_dict(u, wl.get_players_dict(user_stats, players_list))
    # Step 3: Ranking based on top and bottom 10 teammates
    list_for_tops = wl.get_overall_wr(user_stats, players_list)
    rank_all_players[user] = wl.get_top_bottom_lists(list_for_tops, top)
    global_ranking = wl.assign_weights(global_ranking, user, rank_all_players[user][0], 'top')
    global_ranking = wl.assign_weights(global_ranking, user, rank_all_players[user][1], 'bottom')
    # Step 4: Ranking based on preference
    pref = wl.get_preference(list_for_tops)
    global_pref = wl.assign_pref(global_pref, pref)
    # Step 5: Teams winrate
    teams = wl.group_by_teams(user_stats)
    global_teams |= teams
    # Step 6: Winrate per hour
    global_hours[user] = wl.get_hours(user_stats)
    # Step 7: Games with purple players
    # global_purples[user] = purples.count_purples(user, items)
    # Step 8: End condition
    global_conditions[user] = e.count_conditions(user_stats)
    # Step 9: Total max scores
    global_scores[user] = t.get_total_scores(user)
    # Step 10: Notes portrait and count
    user_portrait, user_notes_count = np.get_notes_stats(user, user_stats)
    global_portraits[user] = user_portrait
    user_portrait = {k: v for k, v in sorted(user_portrait.items(), key=lambda x: (-x[1], x[0]))}
    np.save(user, user_portrait)
    global_notes_count[user] = user_notes_count
    # Step 11: Notes rate
    global_notes_rates[user] = nr.get_notes_rate(user, user_stats)
    # Step 12: Time spent
    global_times[user] = time.get_times(user_stats)
    # Step 13: Alice wr
    global_Alice[user] = st.get_alice_wr(user, user_stats)
    logger.info(f'Time spent: {u.time_spent(start_time)}')


def main():
    global global_pref, global_times

    for current_user in users:
        main_user(current_user)

    # Save everything
    # up_to_date_stats.tsv
    u.save_up_to_date_stats(up_to_date_stats)
    # winrate/highest_wr.tsv
    u.save_wr(up_to_date_stats)

    # rank/rank_avg.tsv
    for k, v in global_ranking.items():
        global_ranking[k][0] = u.p1(v[0], v[3])
    u.save_ranking(global_ranking, rank_all_players)

    # preference.tsv
    global_pref = wl.update_avg_pref(global_pref)
    u.save_header('output/preference', ['Username', 'Preference'])
    u.save_value('output/preference', u.sort_by_value(global_pref))

    # winrate/teams.tsv
    for k, v in global_teams.items():
        global_teams[k]['win'] = u.p(v['win'], v['loss'])
    u.save_data(u.sort(global_teams, 'win'), 'teams_wr', 'Team')

    for k, v in global_hours.items():
        for k1, v1 in v.items():
            global_hours[k][k1]['win'] = u.p(v1['win'], v1['loss'])
    # time/hours_wr.tsv
    u.save_hours(u.sort_by_key(global_hours), hours_header)
    # time/plots/user.png
    u.save_plots(global_hours, hours_header)
    # end_condition.tsv
    e.save(e.sort_terminated(global_conditions))
    # total_max_scores.tsv
    u.save(
        'output/total_max_scores',
        u.sort(global_scores, 5),
        ['Player', '2p', '3p', '4p', '5p', '6p', 'Total scores']
    )
    # notes/notes_count.tsv
    u.save_header(
        'output/notes/notes_count',
        ['Note', 'Per game', 'Total']
    )
    for user in u.sort(global_notes_count, 'count').keys():
        np.save_count(user, global_notes_count[user])
    # notes/notes_rates.tsv
    u.save_header('output/notes/notes_rates', ['Player', 'Rate'])
    for user, user_rate in u.sort_by_value(global_notes_rates).items():
        u.save_value(
            'output/notes/notes_rate',
            {user: user_rate}
        )
    # notes/vocabulary_intersection.tsv
    npa.save(npa.get_voc_comparison(u.sort_by_key(global_portraits)))
    # frequent_words.tsv
    npa.save_words(npa.most_frequent(global_portraits), users)
    # time/time_spent.tsv
    global_times = {k: [u.convert_sec_to_day(v[0]), round(v[1], 1), round(v[2], 1), round(v[3], 1)]
                    for k, v in u.sort(global_times, 0).items()}
    time.save(global_times)
    # winrate/alice/starting_player.tsv
    u.save('output/winrate/alice/starting_player', u.sort(global_Alice, 0), [
        'Player',
        'Ratio',
        'Alice\'s wins',
        'Num games being Alice',
        '!Alice\'s wins',
        'Num games not being Alice'
    ])


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    mlogger = logging.getLogger('matplotlib')
    mlogger.setLevel(logging.WARNING)

    users = u.open_file('input/list_of_players_notes.txt')
    # Init global variables
    up_to_date_stats = {}
    top = 5
    rank_all_players = {k: [] for k in users}
    global_ranking = {k: [0, [], [], 0] for k in users}
    global_pref = {k: [0, 0] for k in users}
    global_teams = {}
    global_hours = {}
    hours_header = [u.add_zero(i) for i in range(0, 24)]
    global_purples = {}
    global_conditions = {}
    global_scores = {}
    global_portraits = {}
    global_notes_count = {}
    global_notes_rates = {}
    global_times = {}
    global_Alice = {}
    main()

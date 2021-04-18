import py.parsing as prs
import py.players as pl
import py.calc as c
import csv


# def change_y():
#     return offset_y + 10

def r(num):
    return str(num).replace('.', ',')


def pr(caption, u_list):
    print(caption)
    print('{}% ({}) / {}% ({})'.format(
        u_list['total_p'][0],
        u_list['total_c'][0],
        u_list['total_p'][1],
        u_list['total_c'][1])
    )
    print('2p totals:')
    print('{}% ({}) / {}% ({})'.format(
        u_list['total_2p_p'][0],
        u_list['total_2p_c'][0],
        u_list['total_2p_p'][1],
        u_list['total_2p_c'][1])
    )
    print('3p totals:')
    print('{}% ({}) / {}% ({})'.format(
        u_list['total_3p_p'][0],
        u_list['total_3p_c'][0],
        u_list['total_3p_p'][1],
        u_list['total_3p_c'][1])
    )


with open(f'../other_files/list_of_users.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

offset_y = 0
results = {}
for u in users:
    # print(u)
    # # parsing
    # history_table = prs.get_history_table(u)
    # items = prs.get_stats(history_table)
    # prs.save_stats(items, u)
    # prs.save_list_of_players(items, u)
    # # set of players
    # pl.save_players_list(pl.create_players_set(u), u)

    # save to excel
    # offset_x = 2
    # print('3', u, offset_x, offset_y)
    # writer = c.get_writer('all')
    totals, totals_easy, totals_sd, totals_null, totals_dd = c.get_all_stats(u)
    # pr('Totals:', totals)
    # pr('Easy:', totals_easy)
    # pr('Easy nulls:', totals_null)
    # pr('Single dark:', totals_sd)
    # pr('Double dark:', totals_dd)

    results[u] = c.get_all_stats(u)

    # print(u, c.get_all_stats(u))
    # offset_x = c.save_to_file(totals, 'Totals', u, writer, offset_x, offset_y)
    # offset_x = c.save_to_file(totals_easy, 'Easy', u, writer, offset_x, offset_y)
    # offset_x = c.save_to_file(totals_sd, 'Single dark', u, writer, offset_x, offset_y)
    # offset_x = c.save_to_file(totals_null, 'Easy null', u, writer, offset_x, offset_y)
    # offset_x = c.save_to_file(totals_dd, 'Double dark', u, writer, offset_x, offset_y)
    # offset_y = change_y()
    # writer.save()

# exec(open('parsing.py').read())
# exec(open('players.py').read())
# exec(open('calc.py').read())
print('Data is generated.')
# print(results)

with open(f'../user_files/all_stat.csv', 'w', newline='') as f:
    w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Username', 'Type', 'W(%)', 'L(%)', 'W(#)', 'L(#)',
                'W(%, 2p)', 'L(%, 2p)', 'W(#, 2p)', 'L(#, 2p)',
                'W(%, 3p+)', 'L(%, 3p+)', 'W(#, 3p+)', 'L(#, 3p+)'])
    for k, v in results.items():
        # print(v)
        # f.write('{}\n'.format(k))
        # w.writerow([k])
        for k1, t in v.items():
            # w.writerow([k1])
            # text = k1
            # if k1 == 'Totals:':
            #     text = k
            w.writerow([
                k,
                k1,
                r(t['total_p'][0]),
                r(t['total_p'][1]),
                t['total_c'][0],
                t['total_c'][1],
                r(t['total_2p_p'][0]),
                r(t['total_2p_p'][1]),
                t['total_2p_c'][0],
                t['total_2p_c'][1],
                r(t['total_3p_p'][0]),
                r(t['total_3p_p'][1]),
                t['total_3p_c'][0],
                t['total_3p_c'][1]]
            )
        #     f.write('{}\nTotals:\t{}\t{}\t{}\t{}\t2p totals:\t{}\t{}\t{}\t{}\t3p totals:\t{}\t{}\t{}\t{}\n'.format(
        #         k1,
        #         t['total_p'][0],
        #         t['total_c'][0],
        #         t['total_p'][1],
        #         t['total_c'][1],
        #         t['total_2p_p'][0],
        #         t['total_2p_c'][0],
        #         t['total_2p_p'][1],
        #         t['total_2p_c'][1],
        #         t['total_3p_p'][0],
        #         t['total_3p_c'][0],
        #         t['total_3p_p'][1],
        #         t['total_3p_c'][1]
        #     ))
        # f.write('\n')

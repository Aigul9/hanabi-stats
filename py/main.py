import py.parsing as prs
import py.players as pl
import py.calc as c


def change_y():
    return offset_y + 10


with open(f'../other_files/list_of_users.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]

offset_y = 0
for u in users:
    # # parsing
    # history_table = prs.get_history_table(u)
    # items = prs.get_stats(history_table)
    # prs.save_stats(items, u)
    # prs.save_list_of_players(items, u)
    # # set of players
    # pl.save_players_list(pl.create_players_set(u), u)
    # save to excel
    offset_x = 2
    # print('3', u, offset_x, offset_y)
    writer = c.get_writer('all')
    totals, totals_easy, totals_sd, totals_null, totals_dd = c.get_all_stats(u)
    print(u, c.get_all_stats(u))
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

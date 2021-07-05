import py.HQL.HQL as h


user = 'Valetta6789'
stats = h.open_stats(user)
stats = h.filter_equal('numPlayers', 2, True)
print(stats)

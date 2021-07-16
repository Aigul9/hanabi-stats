from matplotlib import pyplot as plt

import py.utils as ut

count_games = ut.open_tsv('../output/Result_4.tsv')[:-1]
count = [int(r[2]) for r in count_games]
time = [', '.join([r[0]] + [r[1]]) for r in count_games]
plt.figure(figsize=(40, 5))
plt.xlabel('Month, Year')
plt.ylabel('Number of games')
plt.scatter(time, count)
for i, txt in enumerate(count):
    plt.annotate(txt, (time[i], count[i]))
plt.title('Games per month')
plt.plot(time, count)
plt.savefig(f'../output/games_per_month_speedruns.jpg')

import csv
import networkx as nx
from networkx.algorithms import community

import py.utils as u


G = nx.Graph()
players = []
with open('data/cut version/players_cut.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        players.append(line.rstrip('\n'))


G.add_nodes_from(players)
print(G)
# Graph with 49992 nodes and 0 edges

weights_all = u.open_csv('data/cut version/weights_cut.csv')
for w in weights_all:
    G.add_edge(w[0], w[1], weight=w[2], type='rel')
print(G)
# Graph with 49992 nodes and 126238 edges

# weights_easy = u.open_csv('data/easy, hard relationships/weights_easy.csv')
# for w in weights_easy:
#     G.add_edge(w[0], w[1], weight=w[2], type='easy')
# print(G)
#
# weights_hard = u.open_csv('data/easy, hard relationships/weights_hard.csv')
# for w in weights_hard:
#     G.add_edge(w[0], w[1], weight=w[2], type='hard')
# print(G)

pr = nx.pagerank(G)
# print(pr)
print('--pagerank--')

communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
next_level_communities = next(communities_generator)
res = sorted(map(sorted, next_level_communities))
# print(res)
print('--community--')

f = open('pagerank.csv', 'w', encoding='UTF-8', newline='')
w = csv.writer(f)
for p in players:
    print(p)
    p_pr = pr[p]
    p_com = res.index([r for r in res if p in r][0])
    w.writerow([p, p_pr, p_com])
f.close()

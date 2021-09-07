# Hanabi stats

The program parses users' statistics from https://hanab.live/, calculates percentage of wins and losses for each type of variants (easy, single dark, double dark, easy null variants which are neither single nor double dark), filters it by each player, gets highest winrate, rank, preference, draws plots based on online activity and saves all statistics to the files in tsv format.

Last available results can be found here: [click](https://github.com/Aigul9/hanabi-stats/blob/master/output) (15/06/2021).<br/>

## Stack of technologies
- [Python 3.9](https://www.python.org/)

## Folders structure
- ```docs```: documentation for HQL;
- ```input```: data which should be provided to the program;
- ```output```: results;
- ```py```: python scripts to download and parse statistics, calculate user data;
- ```resources```: list of available variants and their efficiency.

## Output content
- ```filtered_by_players```: list of teammates sorted by win/loss ratio with at least 20 games in total;
- ```misc```: files for my own usage;
- ```plots```: players' activity charts;
- ```rank```: global hanabi rank ([see below](#rank-calculation-algorithm));
- ```wr```: winrate using different sets of variants;
- ```preference.tsv```: weighted sum of positions in the lists of other players;
- ```purples.tsv```: number of games played with purple players;
- ```teams_wr.tsv```: best hanabi teams by wr (>= 50 games, excluding speedrun variants);
- ```up_to_date_stats.tsv```: total statistics group by variant types.

## Types of variants

BGA variants:
- No Variant
- 6 Suits
- Rainbow (6 Suits)

## Rank calculation algorithm
1. Exclude double dark variants.
2. Exclude teammates with less than 100 games.
3. Sort the list by win/loss ratio and divide it into two parts.
4. Select top 5 and bottom 5 teammates (or less if not possible). Player in the middle includes in the list with the closest W/L ([see below](#the-tables-structure)).
5. If the player contains in the these lists, increase or decrease their rank from 1 to 5 depending on the place: for instance, the first player in the top 5 list receives +5 points, the last player in the bottom 5 list receives -5 points.
6. To sum up, the rank shows the frequency of wins with different players.

## Usage
1. Type list of players in ```input/list_of_users.txt```
2. Run script ```main.py```
3. See the results in the ```output``` folder.
4. Parsing and calculations take 1.5s per player in average.

## The tables structure

symbol | description
-|-
W | number of wins
L | number of losses
W/L | win/loss ratio
% | percentage
\# | count (speedruns included)
2p | 2-player games
3p+ | 3-6 player games

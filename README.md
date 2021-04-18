# Hanabi stats

The program parses users' statistics from https://hanab.live/, calculates percentage of winnings and losings for each type of variants (easy, single dark, double dark, easy null variants which are neither single nor double dark) and saves it to the file in tsv format.

## Stack of technologies
- [Python 3.9](https://www.python.org/)

## Folders content
- ```input```: data which should be provided to the program
- ```output```: results
- ```py```: python scripts to download and parse statistics, calculate user values
- ```resources```: list of available variants and their efficiency
- ```temp```: temporary files generated by program, files ```[username]_stats.txt``` and ```[username]_players.txt``` contain table of games and list of players respectively

## Usage
1. Type list of players in ```input/list_of_users.txt```
2. Run script ```main.py```
3. See the results in the ```output/all_stats_[timestamp].tsv```

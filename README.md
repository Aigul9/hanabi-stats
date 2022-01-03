# Hanabi stats

The program parses users' statistics from https://hanab.live/, calculates percentage of wins and losses, filters it by each player, gets highest winrate, rank, preference, draws plots based on online activity and saves all statistics to the files in tsv format.

See graph visualization here: https://aigul9.github.io/hanabi-stats-vis/ (db might be frozen due to non-usage)

See source code: https://github.com/Aigul9/hanabi-stats-vis

## Stack of technologies
- [Python 3.9](https://www.python.org/)
- [PostgreSQL 13](https://www.postgresql.org/)
- [Docker 20.10](https://www.docker.com/)
- [Neo4j 4.3](https://neo4j.com/)
- [Swagger 2.0](https://swagger.io/)
- [pdoc 3](https://pdoc3.github.io/pdoc/)

## Folders structure
- ```database```: python and sql scripts related to PostgreSQL;
- ```docs```: documentation of the main methods;
- ```input```: data which should be provided to the program;
- ```neo4j```: scripts and generated data fed into neo4j database;
- ```output```: results;
- ```py```: python scripts to download and parse statistics, calculate user data;
- ```py```: undocumented python scripts;
- ```resources```: list of available variants and their efficiency;
- ```swagger```: API documentation.

## Rank calculation algorithm
1. Exclude double dark variants.
2. Exclude teammates with less than 100 games.
3. Sort the list by win/loss ratio and divide it into two parts.
4. Select top 5 and bottom 5 teammates (or less if not possible). Player in the middle includes in the list with the closest W/L ([see below](#the-tables-structure)).
5. If the player contains in the these lists, increase or decrease their rank from 1 to 5 depending on the place: for instance, the first player in the top 5 list receives +5 points, the last player in the bottom 5 list receives -5 points.
6. To sum up, the rank shows the frequency of wins with different players.

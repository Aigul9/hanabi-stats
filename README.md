# Hanabi stats

The program loads users' games and actions from https://hanab.live/ via api, feeds it in the database, calculates various statistics, and saves them to files in tsv format. <kbd>test<kbd>

Code documentation: https://aigul9.github.io/hanabi-stats/

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
- ```docs```: documentation of the python functions;
- ```input```: data which should be provided to the program;
- ```neo4j```: scripts and generated data fed into neo4j database;
- ```output```: results;
- ```py```: python scripts to download and parse statistics, calculate user data;
- ```resources```: list of available variants and their efficiency;
- ```swagger```: API documentation.

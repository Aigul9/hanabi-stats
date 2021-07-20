import json
import logging

import database.db_load as d
import py.utils as u


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
hanabi_players = u.open_file('../output/unnest_players_character_varying_.tsv')
for p in hanabi_players:
    try:
        stats = u.open_stats(p)
    except json.decoder.JSONDecodeError:
        logger.error(p)
        continue
    for s in stats:
        d.update_game(s)
    d.session.commit()
    logger.info(p)

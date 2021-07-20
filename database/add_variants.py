import logging

import sqlalchemy

import database.db_load as d
import py.utils as u
from database.db_connect import session, Variant


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
variants = u.open_tsv('../resources/variants_id.tsv')
for v in variants:
    var = session.query(Variant).filter(Variant.variant_id == v[1]).first()
    if var is None:
        d.load_variant(v[0][:-1], v[1][1:])
        d.session.commit()
    logger.info(v)

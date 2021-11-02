import json

from database.db_connect import session, Variant


with open('../../resources/variants_1103.json', "r") as variants_file:
    variants = json.loads(variants_file.read())

for v in variants:
    print(v)
    variant = session.query(Variant).filter(Variant.variant == v['name']).first()
    if variant.suits:
        continue
    variant.suits = v['suits']
    session.commit()
session.close()

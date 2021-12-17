import py.utils as u
from database.db_connect import session, Variant


with open('../resources/variant_types.txt', 'r', encoding='utf-8') as f:
    variants = {}
    for line in f.readlines():
        line = line.rstrip().split('\t')
        if 'null' in line[1]:
            line[1] = line[1].replace(' null', '')
        variants[line[0]] = line[1]

with open('../resources/types_from_doc.txt', 'r', encoding='utf-8') as f:
    variant_types = {}
    for line in f.readlines():
        line = line.rstrip().split('\t')
        variant_types[line[0]] = [line[1], line[2], line[3], line[4]]

variants_db = session.query(Variant).all()
for v in variants_db:
    v.eff_2p = float(variant_types[variants[v.variant]][0].replace(',', '.'))
    v.eff_34p = float(variant_types[variants[v.variant]][1].replace(',', '.'))
    v.eff_5p = float(variant_types[variants[v.variant]][2].replace(',', '.'))
    v.eff_6p = float(variant_types[variants[v.variant]][3].replace(',', '.'))
    session.commit()

session.close()

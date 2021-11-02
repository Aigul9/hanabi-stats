import json
import logging

import database.db_load as d
import py.utils as u
from database.db_connect import session, Variant


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# variants = u.open_tsv('../resources/variants_id.tsv')
# for v in variants:
#     var = session.query(Variant).filter(Variant.variant_id == v[1]).first()
#     if var is None:
#         d.load_variant(v[0][:-1], v[1][1:])
#         d.session.commit()
#     logger.info(v)

with open('../../resources/variants_1103.json', "r") as variants_file:
    variants = json.loads(variants_file.read())

with open('../../resources/suits.json', "r") as suits_file:
    suits_json = json.loads(suits_file.read())

colors = ['Red', 'Yellow', 'Green', 'Blue', 'Purple', 'Teal', 'Black', 'Pink', 'Brown']
for v in variants:
    variant = session.query(Variant).filter(Variant.variant == v['name']).first()
    if variant.colors:
        continue
    logger.info(v['name'])
    suits = variant.suits
    var_colors = []
    var_clue_colors = set()
    for s in suits:
        s_json = [sj for sj in suits_json if sj['name'] == s][0]
        if 'clueColors' in s_json:
            clue_colors = s_json['clueColors']
            # print(clue_colors)
            var_clue_colors |= set(clue_colors)
    # for c in colors:
    #     if c in var_clue_colors:
    #         var_colors.append(c)
    # variant.colors = var_colors
    # print(var_colors)

        if s in colors:
            var_colors.append(s)
        if s == 'Dark Pink':
            var_colors.append('Pink')
        if s == 'Dark Brown':
            var_colors.append('Brown')
    variant.colors = var_colors
    variant.suits = v['suits']
    # if 'specialRank' in v:
    #     variant.special_rank = v['specialRank']
    # if 'specialDeceptive' in v:
    #     variant.special_deceptive = v['specialDeceptive']
    # if 'specialAllClueColors' in v:
    #     variant.special_all_clue_colors = v['specialAllClueColors']
    # if 'specialAllClueRanks' in v:
    #     variant.special_all_clue_ranks = v['specialAllClueRanks']
    # if 'specialNoClueColors' in v:
    #     variant.special_no_clue_colors = v['specialNoClueColors']
    # if 'specialNoClueRanks' in v:
    #     variant.special_no_clue_ranks = v['specialNoClueRanks']
    session.commit()

session.close()

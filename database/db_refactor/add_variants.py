import base64
import json
import logging
import requests

from database.db_connect import session, Variant
from database.db_load import load_variant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def req_json(url):
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.json()
        content = base64.b64decode(req['content'])
        return json.loads(content)
    else:
        logger.error('Content was not found.')
        exit()


def get_colors(variant):
    colors_list = ['Red', 'Yellow', 'Green', 'Blue', 'Purple', 'Teal', 'Black', 'Pink', 'Brown']
    suits = variant['suits']
    var_colors = list()
    for s in suits:
        # we need a 'clueColors' prop from the suits_json
        s_json = [sj for sj in suits_json if sj['name'] == s][0]
        if 'clueColors' in s_json:
            # add each color separately without duplicates
            for cc in s_json['clueColors']:
                if cc not in var_colors:
                    var_colors.append(cc)
        # otherwise, color = suit name
        elif s in colors_list:
            if s not in var_colors:
                var_colors.append(s)
    return var_colors


# https://github.com/Hanabi-Live/hanabi-live/tree/main/packages/data/src/json
url_var = 'https://api.github.com/repos/Hanabi-Live/hanabi-live/contents/packages/data/src/json/variants.json'
url_suits = 'https://api.github.com/repos/Hanabi-Live/hanabi-live/contents/packages/data/src/json/suits.json'
variants_json = req_json(url_var)
suits_json = req_json(url_suits)
for v in variants_json:
    var = session.query(Variant).filter(Variant.variant_id == v['id']).first()
    if var is None:
        colors = get_colors(v)
        load_variant(v, colors)
        logger.info(v)
    session.commit()

session.close()

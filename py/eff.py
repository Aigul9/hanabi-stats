class Variant:
    def __init__(self, variant, var_doctype='', var_type=''):
        self.variant = variant
        self.var_doctype = var_doctype
        self.var_type = var_type


def __iter__(self):
    return iter((self.variant, self.var_doctype, self.var_type))


with open('../resources/1oE_variants.txt', 'r') as f:
    unique_var = []
    for line in f.readlines():
        unique_var.append(line.strip())


with open('../resources/variants.txt', 'r') as f:
    all_var = []
    for line in f.readlines():
        line = line.strip()
        all_var.append(Variant(line[:line.rfind('(') - 1]))

cases = {
    '6 Suits': '6 Suits',
    'No Variant': '5 Suits',
    '4 Suits': '4 Suits',
    '3 Suits': '3 Suits',
    'Up or Down (6 Suits)': '6 Suits (Up or Down)',
    'Up or Down (5 Suits)': '5 Suits (Up or Down)',
    'Throw It in a Hole (6 Suits)': '6 Suits (Throw It in a Hole)',
    'Throw It in a Hole (5 Suits)': '5 Suits (Throw It in a Hole)',
    'Throw It in a Hole (4 Suits)': '4 Suits (Throw It in a Hole)',
    'Clue Starved (6 Suits)': '6 Suits (Clue Starved)',
    'Clue Starved (5 Suits)': '5 Suits (Clue Starved)'
}

for row in all_var:
    v = row.variant
    if v in cases:
        row.var_doctype, row.var_type = cases[v], 'easy'
        continue
    if 'Null' in v:
        row.var_doctype = row.var_type = 'null'
    uv = [uv for uv in unique_var if (uv in v)]
    if len(uv) == 1:
        row.var_doctype, row.var_type = 'w/ 1x 1oE', 'sd'
    if len(uv) == 3:
        row.var_doctype, row.var_type = 'w/ 2x 1oE', 'dd'
    if len(uv) == 2:
        row.var_doctype = 'w/ 1x 1oE' if 'Gray Pink' in uv else 'w/ 2x 1oE'
        row.var_type = 'sd' if 'Gray Pink' in uv else 'dd'
    row.var_type = row.var_type if row.var_doctype else 'easy'
    row.var_doctype = v[-8:-1] + ' ' + row.var_doctype if row.var_doctype else v[-8:-1]

with open('../resources/variant_types.txt', 'w') as f:
    for row in all_var:
        v, d, t = __iter__(row)
        f.write('{}\t{}\t{}\n'.format(v, d, t))

# all_var.sort(key=lambda var: len(var.variant), reverse=True)
# with open('../resources/variants_sorted.txt', 'w') as f:
#     for row in all_var:
#         v, d, t = __iter__(row)
#         f.write('{}\t{}\n'.format(v, len(v)))

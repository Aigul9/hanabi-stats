with open('other_files/1oE_variants.txt', 'r') as f:
    unique_var = []
    for line in f.readlines():
        unique_var.append(line.strip())

# print(unique_var)

with open('other_files/variants.txt', 'r') as f:
    all_var = {}
    for line in f.readlines():
        line = line.strip()
        all_var[line[:line.rfind('(') - 1]] = ""

# print(all_var)

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

for k in all_var.keys():
    if k in cases:
        all_var[k] = cases[k]
        continue
    # if 'Null' in k:
    #     all_var[k] = 'Null'
    uv = [uv for uv in unique_var if(uv in k)]
    if len(uv) == 1:
        all_var[k] = "w/ 1x 1oE"
    if len(uv) == 3:
        all_var[k] = "w/ 2x 1oE"
    if len(uv) == 2:
        all_var[k] = "w/ 1x 1oE" if 'Gray Pink' in uv else "w/ 2x 1oE"
    all_var[k] = k[-8:-1] + ' ' + all_var[k] if all_var[k] else k[-8:-1]
    # print(all_var[k])

# print(all_var)

with open('other_files/variant_types.txt', 'w') as f:
    f.write('Variant\tType\n')
    for k, v in all_var.items():
        # print(v)
        f.write('%s\t%s\n' % k % v)

# for k, v in all_var.items():
#     if v == '':
#         print(k)

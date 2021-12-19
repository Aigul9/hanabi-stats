import csv

import py_no_doc.utils as u


weights_easy = u.open_csv('weights_easy.csv')
weights_hard = u.open_csv('weights_hard.csv')
removed = u.open_csv('removed.csv')
removed = [r[0] for r in removed]

f_easy = open('weights_easy_r.csv', 'w', encoding='UTF-8', newline='')
f_hard = open('weights_hard_r.csv', 'w', encoding='UTF-8', newline='')

w_easy = csv.writer(f_easy)
w_hard = csv.writer(f_hard)

remove_list = [
    'superbipbip',
    'Pimak',
    'sheamol',
    'sckuzzle',
    'Fafrd',
    'cequoy',
    'scepheo',
    'Elatekur',
    'Shos',
    'Ptheven',
    'skyblueexo',
    'nmego',
    'Kaznad',
    'JDepp',
    'Carunty',
    'honzas',
    'MasN',
    'Bonja',
    'cak199164',
    'CaptainAggro',
    'castlesintheair',
    'Floribster',
    'Gazrovor',
    '910dan',
    'yaiir',
    'Swifter',
    'MarcLovesDogs',
    'Lobsterosity',
    'lotem',
    'rotem',
    'LaFayette',
    'Kernel',
    'katian',
    'indegoo',
    'fpvandoorn',
    'Floribster',
    'Etherealz',
    'eljobe',
    'eljavi',
    'elamate',
    'Doge',
    'smallman',
    'wjomlex',
    'postmans',
    'Onen',
    'Hoodie',
    'Chronometrics',
    'colton',
    'Div',
    'awe',
    'Asddsa76',
    'Animex52',
    'Amy2',
    'xor',
    'sankala fan',
    'XMIL',
    'MKQ',
    'Matze22',
    'methmatics',
    'Daryl',
    'Tiramisu2th',
    'TheDaniMan',
    'qqqq',
    'ksforston',
    'efaust'
]

for w in weights_easy:
    print(w)
    if w[0] in removed or w[1] in removed:
        continue
    else:
        w_easy.writerow(w)
    # if w[1] not in removed:

f_easy.close()

print('------------------------')

for w in weights_hard:
    print(w)
    if w[0] in removed or w[1] in removed:
        continue
    else:
        w_hard.writerow(w)

f_hard.close()

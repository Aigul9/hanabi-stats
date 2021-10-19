import csv

import py.utils as u


weights_easy = u.open_csv('weights_easy.csv')
weights_hard = u.open_csv('weights_hard.csv')
removed = u.open_csv('removed.csv')

f_easy = open('weights_easy.csv', 'w', encoding='UTF-8', newline='')
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
    if w[0] in remove_list or w[1] in remove_list:
        continue
    else:
        w_easy.writerow(w)
    # if w[1] not in removed:

f_easy.close()

print('------------------------')

for w in weights_hard:
    print(w)
    if w[0] in remove_list or w[1] in remove_list:
        continue
    else:
        w_hard.writerow(w)

f_hard.close()

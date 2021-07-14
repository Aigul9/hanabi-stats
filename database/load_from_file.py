import json
import py.utils as ut


path = '../temp/games_dumps/'
files = ut.files_in_dir(path)


def open_as_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = {}
        for line in file.readlines():
            try:
                line_dict = json.loads(line.rstrip())
                data[line_dict['id']] = line_dict
            except json.decoder.JSONDecodeError:
                print(line)
                exit()
        return data


def load_games():
    games = {}
    for f in files:
        print(f)
        games = games | open_as_json(f'{path}{f}')
    return games

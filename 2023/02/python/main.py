#!/usr/bin/env python3

import re


INPUT = './test.txt' if (TEST := False) else './input.txt'


def parse_line(line):
    fields = re.split(r'\s', line)

    game_id = int(fields[1][:-1])

    subsets = [{}]

    index = 2

    while index < len(fields):
        field = fields[index]

        amount = int(field)

        index += 1 # get name

        name = fields[index]

        starts_new_list = name[-1] == ';'
        has_comma = name[-1] == ','

        name = name[:-1] if starts_new_list or has_comma else name

        subsets[-1][name] = subsets[-1].get(name, 0) + amount

        if starts_new_list:
            subsets.append({})

        index += 1

    return {
        'game_id': game_id,
        'subsets': subsets
    }


games = [parse_line(line) for line in re.split(r'\n', open(INPUT, 'r').read().strip())]

RED = 12
GREEN = 13
BLUE = 14

bag = {
    'red': RED,
    'green': GREEN,
    'blue': BLUE
}

def restore_bag(out=None):
    bag['red'] = RED
    bag['green'] = GREEN
    bag['blue'] = BLUE
    return out


def is_game_possible(game):
    for subset in game['subsets']:
        for key, value in subset.items():
            if bag[key] - value < 0:
                return restore_bag(False)

            bag[key] -= value

        restore_bag()

    return True

possible_game_ids_sum = sum([game['game_id'] if is_game_possible(game) else 0 for game in games])


print('P1:', possible_game_ids_sum)

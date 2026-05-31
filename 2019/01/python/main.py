#!/usr/bin/env python3

import re

file = './input.txt'

data = re.split(r'\n|\s', open(file, 'r').read())

part_one = sum([int(x) // 3 - 2 for x in data if x != ''])

print(f'P1: {part_one}')

def calc_fuel(of):
    result = 0
    of = of // 3 - 2

    while of > 0:
        result += of

        of = of // 3 - 2

    return result

part_two = sum([calc_fuel(int(x)) for x in data if x != ''])

print(f'P2: {part_two}')

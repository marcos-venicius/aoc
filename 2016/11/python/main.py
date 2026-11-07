#!/usr/bin/env python3

import re

ORDINAL_MAP = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3
}

TEST = False

if TEST:
    INPUT = './test.txt'
else:
    INPUT = './input.txt'

# 1. it can carry at most yourself and two RTGs or microchips in any combination
# 2. the elevator will only function if it contains at least one RTG or microchip
# 3. The elevator always stops on each floor to recharge, and this takes long enough that the items within it and the items on that floor can irradiate each other
# 4. You can prevent this if a Microchip and its Generator end up on the same floor in this way, as they can be connected while the elevator is recharging.
# 5. you and the elevator will start on the first floor

def parse_line(line):
    tokens = list(filter(lambda x: x.strip() != '', re.findall(r'(?:\w+(?:-\w+)?)|[,. ]', line)))

    cursor = 0
    size   = len(tokens)
    token  = lambda: tokens[cursor]
    output = lambda: { 'floor': floor, 'data': data }

    floor = None
    data = {}

    cursor += 1 # skip 'The'

    floor = ORDINAL_MAP[token()]

    cursor += 1 # skip the floor
    cursor += 1 # skip 'floor'
    cursor += 1 # skip 'contains'

    if token() == 'nothing':
        return output()

    while cursor < size:
        if token() == 'and' or token() == ',' or token() == '.':
            cursor += 1 # skip 'and'
            continue

        cursor += 1 # skip 'a'

        component = token().replace('-compatible', '')

        cursor += 1 # skip component

        kind = token()

        cursor += 1 # skip kind

        if kind not in data:
            data[kind] = set()

        data[kind].add(component)

    return output()

floors = []

lines = list(map(parse_line, filter(lambda x: x != '', open(INPUT, 'r').read().split('\n'))))

for line in lines:
    if len(floors) <= line['floor']:
        floors = floors + ([{}] * (line['floor'] - len(floors) + 1))

    for key in line['data']:
        if key not in floors[line['floor']]:
            floors[line['floor']][key] = set()

        for value in line['data'][key]:
            floors[line['floor']][key].add(value)


for floor in floors:
    print(floor)

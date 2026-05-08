#!/usr/bin/env python3

import sys


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <input file>')
    exit(1)

lines = open(sys.argv[1], 'r').read().splitlines()

ingredient_ranges = []
fresh_ingredients = 0
all_fresh_ingredients = 0

for i in range(len(lines)):
    line = lines[i]

    if line != '':
        split = line.split('-')

        f, t = int(split[0]), int(split[1])

        ingredient_ranges.append((f, t))
    else:
        ingredient_ranges = sorted(ingredient_ranges, key=lambda x: x[0])

        for line in lines[i+1:]:
            ingredient_id = int(line)

            # TODO: binary search?
            for (f, t) in ingredient_ranges:
                if ingredient_id >= f and ingredient_id <= t:
                    fresh_ingredients += 1
                    break

        break

print(f'P1: {fresh_ingredients}')

f = ingredient_ranges[0][0]
t = ingredient_ranges[0][1]

for i in range(1, len(ingredient_ranges)):
    nxt = ingredient_ranges[i]

    if nxt[0] <= t:
        t = max(t, nxt[1])
    else:
        all_fresh_ingredients += t - f + 1

        f = nxt[0]
        t = nxt[1]

all_fresh_ingredients += t - f + 1

print(f'P2: {all_fresh_ingredients}')

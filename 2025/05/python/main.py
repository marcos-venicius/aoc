#!/usr/bin/env python3

import sys


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <input file>')
    exit(1)

lines = open(sys.argv[1], 'r').read().splitlines()

ingredient_ranges = []
fresh_ingredients = 0

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

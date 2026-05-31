#!/usr/bin/env python3

import re

file = './input.txt'

data = [int(x) for x in re.split(r'\n|\s', open(file, 'r').read()) if x != '']
data = [data[i:i+3] for i in range(0, len(data), 3)]

# check if it's really a triangle (sum the two smallest sides and check if it's greater than the resulting one)
part_one = len([t for t in data if sum(sorted(t)[:-1]) > max(t)])

print(f'P1: {part_one}')

vertical = [[], [], []]

for t in data:
  vertical[0].append(t[0])
  vertical[1].append(t[1])
  vertical[2].append(t[2])

data = vertical[0] + vertical[1] + vertical[2]
data = [data[i:i+3] for i in range(0, len(data), 3)]

part_two = len([t for t in data if sum(sorted(t)[:-1]) > max(t)])

print(f'P2: {part_two}')

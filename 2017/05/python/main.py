#!/usr/bin/env python3

import re

TEST = False

if TEST:
    INPUT = './test.txt'
else:
    INPUT = './input.txt'

offsets = list(map(int, filter(lambda x: x != '', re.split(r'\s', open(INPUT, 'r').read()))))

iterations = 0
index = 0

while index >= 0 and index < len(offsets):
    iterations += 1

    next_index = index + offsets[index]

    offsets[index] += 1

    index = next_index

print(iterations)


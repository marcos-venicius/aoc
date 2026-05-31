#!/usr/bin/env python3

import re

file = './input.txt'

data = [int(x) for x in re.split('\n|\s', open(file, 'r').read()) if x != '']

part_one = 0

for i in range(1, len(data)):
    if data[i] > data[i - 1]:
        part_one += 1

print(f'P1: {part_one}')

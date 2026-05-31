#!/usr/bin/env python3

import re

file = './input.txt'

data = [x for x in re.split(r'\n|\s', open(file, 'r').read()) if x != '']

part_one = 0

for freq in data:
    if freq[0] == '+':
        part_one += int(freq[1:])
    elif freq[0] == '-':
        part_one -= int(freq[1:])
    else:
        raise Exception(f"invalid {freq}")

print(f'P1: {part_one}')

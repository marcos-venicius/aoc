#!/usr/bin/env python3

import re

file = './input.txt'

data = re.split(r'\n|\s', open(file, 'r').read())

part_one = sum([int(x) // 3 - 2 for x in data if x != ''])

print(f'P1: {part_one}')

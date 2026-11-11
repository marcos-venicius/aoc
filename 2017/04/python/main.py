#!/usr/bin/env python3

import re

TEST = False

if TEST:
    INPUT = './test.txt'
else:
    INPUT = './input.txt'

data = [re.split(r'\s', row) for row in filter(lambda x: x != '', re.split(r'\n', open(INPUT, 'r').read()))]

part_one = sum(len(row) == len(set(row)) for row in data)

print('P1:', part_one)
print('P2:')
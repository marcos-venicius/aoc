#!/usr/bin/env python3

import re

file = './input.txt'

data = [list(map(int, re.split(r'\s', x))) for x in open(file, 'r').read().split('\n') if x != '']

part_one = sum([max(x) - min(x) for x in data])

print(f'P1: {part_one}')

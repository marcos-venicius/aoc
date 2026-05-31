#!/usr/bin/env python3

import re

file = './input.txt'

data = [int(x) for x in re.split('\n|\s', open(file, 'r').read()) if x != '']

part_one = 0

for i in range(1, len(data)):
    if data[i] > data[i - 1]:
        part_one += 1

print(f'P1: {part_one}')

part_two = 0

for i in range(len(data) - 3):
    m = data[i + 1] + data[i + 2]

    a = data[i] + m
    b = m + data[i + 3]

    if b > a:
        part_two += 1

print(f'P2: {part_two}')

#!/usr/bin/env python3

import re

file = './input.txt'

data = [list(map(int, re.split(r'\s', x))) for x in open(file, 'r').read().split('\n') if x != '']

part_one = sum([max(x) - min(x) for x in data])

print(f'P1: {part_one}')

def get_divisors(line):
    for i in range(len(line)):
        for j in range(len(line)):
            if i == j: continue

            a = line[i]
            b = line[j]

            if a / b % 1 == 0:
                return a // b

    return 0

part_two = sum([get_divisors(x) for x in data])

print(f'P2: {part_two}')

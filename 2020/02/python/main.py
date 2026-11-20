#!/usr/bin/env python3

import sys
from collections import Counter

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

def parse_line(line):
    tokens = line.split(' ')

    password = tokens[-1]

    mn, mx = list(map(int, tokens[0].split('-')))
    char = tokens[1][:-1]

    return (mn, mx, char, password)


data = [parse_line(line) for line in open(INPUT, 'r').read().strip().split('\n')]

def is_password_valid(info):
    count = dict(Counter(info[-1]))

    return count.get(info[2], -1) >= info[0] and count[info[2]] <= info[1]

part_one = sum(is_password_valid(info) for info in data)

print('P1:', part_one)
print('P2:', None)

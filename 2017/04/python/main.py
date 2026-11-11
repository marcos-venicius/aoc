#!/usr/bin/env python3

import re

TEST = False

if TEST:
    INPUT = './test.txt'
else:
    INPUT = './input.txt'

def check_anagrams(row):
    n = set()

    for word in row:
        s = ''.join(sorted([c for c in word]))

        if s in n:
            return True

        n.add(s)

    return False

data = [re.split(r'\s', row) for row in filter(lambda x: x != '', re.split(r'\n', open(INPUT, 'r').read()))]

part_one = sum(len(row) == len(set(row)) for row in data)
part_two = sum(not check_anagrams(row) for row in data)

print('P1:', part_one)
print('P2:', part_two)
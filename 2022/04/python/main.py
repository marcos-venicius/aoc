#!/usr/bin/env python3

import re

INPUT = './test.txt' if (TEST := False) else './input.txt'

data = [list(map(int, re.split(r',|-', line))) for line in re.split(r'\s', open(INPUT, 'r').read().strip())]

def does_pair_fully_overlaps(pair):
    a, b, x, y = pair

    return (
        (a <= x and b >= y)
        or
        (x <= a and y >= b)
    )

def does_pair_overlap_at_all(pair):
    a, b, x, y = pair

    return min(a, b) <= max(x, y) and max(a, b) >= min(x, y)

part_one = sum([does_pair_fully_overlaps(pair) for pair in data])
part_two = sum([does_pair_overlap_at_all(pair) for pair in data])

print('P1:', part_one)
print('P2:', part_two)
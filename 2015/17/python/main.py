#!/usr/bin/env python3

import re
from itertools import combinations

target = 150
data = [int(a.group(0)) for a in re.finditer(r'\d+', open('./input.txt', 'r').read())]
count = 0

for r in range(1, len(data) + 1):
    for comb in combinations(data, r):
        if sum(comb) == target:
            count += 1

print('P1:', count)

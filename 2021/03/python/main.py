#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

binary = [[c for c in line] for line in open(INPUT, 'r').read().strip().split('\n')]

bits = [{} for _ in range(len(binary[0]))]

for row in binary:
    for i, v in enumerate(row):
        bits[i][v] = bits[i].get(v, 0) + 1

gamma_rate = int(''.join([max(bit.keys(), key=lambda key: bit[key]) for bit in bits]), 2)
epsilon_rate = int(''.join([min(bit.keys(), key=lambda key: bit[key]) for bit in bits]), 2)

part_one = gamma_rate * epsilon_rate

print('P1:', part_one)
print('P2:', None)

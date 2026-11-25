#!/usr/bin/env python3

import sys
from functools import reduce

gamma_rate, epsilon_rate = map(lambda bin: int(''.join(bin), 2), list(reduce(lambda acc, curr: (acc[0] + [max(curr.keys(), key=lambda key: curr[key])], acc[1] + [min(curr.keys(), key=lambda key: curr[key])]), [{'0': row.count('0'), '1': row.count('1')} for row in ([list(row) for row in zip(*[[c for c in line] for line in open('./test.txt' if ('run' not in sys.argv) else './input.txt', 'r').read().strip().split('\n')])])], ([], []))))

print('P1:', gamma_rate * epsilon_rate)
print('P2:', None)

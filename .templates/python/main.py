#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

data = open(INPUT, 'r').read().strip()

print(data)

print('P1:', None)
print('P2:', None)

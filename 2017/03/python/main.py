#!/usr/bin/env python3

import math

# manhathan distance
N = int(input('puzzle input> '))
k = math.ceil((math.sqrt(N) - 1) / 2)
t = 2 * k
M = (t + 1) ** 2
s = M - N


x = 0
y = 0

if s < t:
    x = k - s
    y = k
elif s < 2 * t:
    x = -k
    y = k - (s - t)
elif s < 3 * t:
    x = -k + (s - 2 * t)
    y = -k
else:
    x = k
    y = -k + (s - 3 * t)

d = math.fabs(x) + math.fabs(y)

part_one = int(d)

print(f'P1: {part_one}')

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

def get_part_two():
    grid = {(0, 0): 1}
    x = 0
    y = 0
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    d = 0
    step = 0
    part_two = None

    while part_two is None:
        for _ in range(2):
            dx, dy = dirs[d % 4]

            for _ in range(step):
                x, y = x + dx, y + dy

                v = sum(
                    grid.get((x + i, y + j), 0)
                    for i in (-1, 0, 1)
                    for j in (-1, 0, 1)
                )

                grid[(x, y)] = v

                if v > N:
                    return v
            d += 1
        step += 1
part_one = int(d)

print(f'P1: {part_one}')

part_two = get_part_two()

print(f'P2:', part_two)

#!/usr/bin/env python3

import sys
from time import time

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

def parse_line(line):
    return [(op[0], int(op[1:])) for op in line.split(',')]

wire_one, wire_two = list(map(parse_line, open(INPUT, 'r').read().strip().split('\n')))

DELTAS = {
    'U': (0, -1),
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0)
}

def expand_wire(wire):
    board = {}
    x = 0
    y = 0
    steps = 0

    for op, units in wire:
        dx, dy = DELTAS[op]

        for i in range(1, units + 1):
            x += dx
            y += dy
            board[(x, y)] = steps + i

        steps += units

    return board

start = time()
board_one = expand_wire(wire_one)
board_two = expand_wire(wire_two)

nearest_manhattan_distance = filter(lambda x: x in board_two, sorted(board_one.keys(), key=lambda x: abs(x[0]) + abs(x[1])))

min_distance = None
min_steps = None

for pos in nearest_manhattan_distance:
    distance = abs(pos[0]) + abs(pos[1])

    if min_distance is None:
        min_distance = distance

    steps_sum = board_one[pos] + board_two[pos]

    if min_steps is None or steps_sum < min_steps:
        min_steps = steps_sum

print('P1:', min_distance)
print('P2:', min_steps)

end = time()

elapsed = end - start

print(f'exec time: {elapsed:.3f}s')
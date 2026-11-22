#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

def parse_line(line):
    return [(op[0], int(op[1:])) for op in line.split(',')]

wire_one, wire_two = list(map(parse_line, open(INPUT, 'r').read().strip().split('\n')))

board_one = {}
board_two = {}

x = 0
y = 0

for op, units in wire_one:
    match op:
        case 'U':
            for _ in range(units):
                y -= 1
                board_one[(x, y)] = 1
        case 'R':
            for _ in range(units):
                x += 1
                board_one[(x, y)] = 1
        case 'D':
            for _ in range(units):
                y += 1
                board_one[(x, y)] = 1
        case 'L':
            for _ in range(units):
                x -= 1
                board_one[(x, y)] = 1

x = 0
y = 0

for op, units in wire_two:
    match op:
        case 'U':
            for _ in range(units):
                y -= 1
                board_two[(x, y)] = 1
        case 'R':
            for _ in range(units):
                x += 1
                board_two[(x, y)] = 1
        case 'D':
            for _ in range(units):
                y += 1
                board_two[(x, y)] = 1
        case 'L':
            for _ in range(units):
                x -= 1
                board_two[(x, y)] = 1

min_distance = None

map_one = sorted(board_one.keys(), key=lambda x: abs(x[0]) + abs(x[1]))

for pos_one in map_one:
    if pos_one in board_two:
        distance = abs(pos_one[0]) + abs(pos_one[1])

        if min_distance is None or distance < min_distance:
            min_distance = distance
            break

print('P1:', min_distance)
print('P2:', None)
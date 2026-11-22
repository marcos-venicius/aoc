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
steps = 0

for i, (op, units) in enumerate(wire_one):
    match op:
        case 'U':
            for i in range(units):
                steps += 1
                y -= 1
                if (x, y) not in board_one:
                    board_one[(x, y)] = steps
        case 'R':
            for _ in range(units):
                steps += 1
                x += 1
                if (x, y) not in board_one:
                    board_one[(x, y)] = steps
        case 'D':
            for _ in range(units):
                steps += 1
                y += 1
                if (x, y) not in board_one:
                    board_one[(x, y)] = steps
        case 'L':
            for _ in range(units):
                steps += 1
                x -= 1
                if (x, y) not in board_one:
                    board_one[(x, y)] = steps

x = 0
y = 0
steps = 0

for i, (op, units) in enumerate(wire_two):
    match op:
        case 'U':
            for _ in range(units):
                steps += 1
                y -= 1
                if (x, y) not in board_two:
                    board_two[(x, y)] = steps
        case 'R':
            for _ in range(units):
                steps += 1
                x += 1
                if (x, y) not in board_two:
                    board_two[(x, y)] = steps
        case 'D':
            for _ in range(units):
                steps += 1
                y += 1
                if (x, y) not in board_two:
                    board_two[(x, y)] = steps
        case 'L':
            for _ in range(units):
                steps += 1
                x -= 1
                if (x, y) not in board_two:
                    board_two[(x, y)] = steps

min_distance = None
part_two = None

map_one = sorted(board_one.keys(), key=lambda x: abs(x[0]) + abs(x[1]))

for pos_one in map_one:
    if pos_one in board_two:
        distance = abs(pos_one[0]) + abs(pos_one[1])
        steps_sum = board_two[pos_one] + board_one[pos_one]

        if min_distance is None or distance < min_distance:
            min_distance = distance
        if part_two is None or steps_sum < part_two:
            part_two = steps_sum

print('P1:', min_distance)
print('P2:', part_two)
#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

def parse_line(line):
    direction, units = line.split(' ')

    return (direction, int(units))

lines = [parse_line(line) for line in open(INPUT, 'r').read().strip().split('\n')]

def part_one():
    X = 0
    Y = 0

    for (direction, units) in lines:
        match direction:
            case 'forward':
                X += units
            case 'down':
                Y += units
            case 'up':
                Y -= units

    return X * Y

def part_two():
    AIM = 0
    X = 0
    Y = 0

    for (direction, units) in lines:
        match direction:
            case 'forward':
                X += units
                Y += AIM * units
            case 'down':
                AIM += units
            case 'up':
                AIM -= units

    return X * Y

print('P1:', part_one())
print('P2:', part_two())
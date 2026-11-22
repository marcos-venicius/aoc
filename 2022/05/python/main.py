#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

lines = open(INPUT, 'r').read().split('\n')

class Stack:
    def __init__(self):
        self.stack = []

    def append(self, value):
        self.stack.append(value)

    def stack(self, lst):
        for item in lst:
            self.append(item)

    def pop(self):
        return self.stack.pop(-1)

def get_indexing_zone():
    for i, line in enumerate(lines):
        if not line.lstrip().startswith('1'):
            continue

        indexes = []

        for x, idx in enumerate(line):
            if idx.isnumeric():
                indexes.append((x, int(idx) - 1))

        return (i, indexes)

    raise Exception('something went wrong')


def get_stacks(where, indexes):
    stacks = [Stack() for _ in indexes]

    for i in range(where - 1, -1, -1):
        line = lines[i]

        for (x, idx) in indexes:
            if x < len(line) and line[x] != ' ':
                stacks[idx].append(line[x])

    return stacks

def get_moves(where):
    moves = []

    for line in lines[where+2:]:
        if line == '':
            break

        _, amount, _, origin, _, destination = line.strip().split(' ')

        moves.append((int(amount), int(origin) - 1, int(destination) - 1))

    return moves

where, indexes = get_indexing_zone()

stacks = get_stacks(where, indexes)
moves = get_moves(where)

for amount, origin, destination in moves:
    for _ in range(amount):
        stacks[destination].append(stacks[origin].pop())

part_one = ''.join([stack.stack[-1] for stack in stacks])

print('P1:', part_one)
print('P2:', None)

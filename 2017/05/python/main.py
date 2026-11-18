#!/usr/bin/env python3

import re

TEST = False

if TEST:
    INPUT = './test.txt'
else:
    INPUT = './input.txt'

offsets = list(map(int, filter(lambda x: x != '', re.split(r'\s', open(INPUT, 'r').read()))))

def solver(label, increase_lambda):
    data = offsets[::]
    iterations = 0
    index = 0

    while index >= 0 and index < len(data):
        iterations += 1

        next_index = index + data[index]

        data[index] += increase_lambda(data[index])

        index = next_index

    print(label, iterations)

solver('P1:', lambda _: 1)
solver('P2:', lambda curr: 1 if curr < 3 else -1)


#!/usr/bin/env python3

import re

TEST = False

INPUT = 'test.txt' if TEST else 'input.txt'

data = list(map(int, re.split(r'\s', open(INPUT, 'r').read().strip())))

def reallocate():
    m_i = None

    for i in range(len(data)):
        if m_i is None or data[i] > data[m_i]:
            m_i = i

    blocks = data[m_i]

    data[m_i] = 0

    index = (m_i + 1) % len(data)

    while blocks > 0:
        data[index] += 1

        blocks -= 1
        index = (index + 1) % len(data)

def get_key():
    return ','.join(map(str, data))

seen_before = set()
cycles = 0

while True:
    key = get_key()

    if key in seen_before:
        break

    seen_before.add(key)

    reallocate()
    cycles += 1

print('P1:', cycles)

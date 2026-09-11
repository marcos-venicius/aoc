#!/usr/bin/env python3

import re

def read_aunt_sues():
    out = []

    for line in open('./input.txt', 'r').read().split('\n'):
        if line == '':
            continue

        groups = re.search(r'\w+ (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)', line)

        sue = int(groups.group(1))

        characteristics = {}

        for i in range(2, 8, 2):
            name = groups.group(i)
            value = int(groups.group(i + 1))

            characteristics[name] = value

        out.append({
            'sue': sue,
            'characteristics': characteristics
        })

    return out

def read_characteristics():
    return {k: int(v) for k, v in [line.split(':') for line in open('./characteristics.txt', 'r').read().split('\n') if line != '']}

aunt_sues = read_aunt_sues()
characteristics = read_characteristics()

def comparator(aunt_chars, only_equal=False):
    contains = 0

    fewer = set(['pomeranians', 'goldfish'])
    greater = set(['cats', 'trees'])

    for char in aunt_chars:
        if not only_equal and char in fewer:
            if aunt_chars[char] < characteristics[char]:
                contains += 1
        elif not only_equal and char in greater:
            if aunt_chars[char] > characteristics[char]:
                contains += 1
        elif aunt_chars[char] == characteristics[char]:
            contains += 1

        if contains == 3:
            return True

    return False

ans_count = 0

for aunt_sue in aunt_sues:
    if comparator(aunt_sue['characteristics'], True):
        print('P1:', aunt_sue['sue'])
        ans_count += 1

    if comparator(aunt_sue['characteristics']):
        print('P2:', aunt_sue['sue'])
        ans_count += 1

    if ans_count == 2:
        break

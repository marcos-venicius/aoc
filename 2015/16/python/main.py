#!/usr/bin/env python3

import re

def read_aunt_sues():
    mx = {}
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

            if name not in mx or mx[name] < value:
                mx[name] = value

        out.append({
            'sue': sue,
            'characteristics': characteristics,
            'rank': 0
        })

    return (out, mx)

def read_characteristics():
    return {k: int(v) for k, v in [line.split(':') for line in open('./characteristics.txt', 'r').read().split('\n') if line != '']}

aunt_sues, mx = read_aunt_sues()
characteristics = read_characteristics()

def comparator(aunt_chars):
    contains = 0

    fewer = set(['pomeranians', 'goldfish'])
    greater = set(['cats', 'trees'])

    for char in aunt_chars:
        if char in fewer:
            if aunt_chars[char] < characteristics[char]:
                contains += 1
        elif char in greater:
            if aunt_chars[char] > characteristics[char]:
                contains += 1
        elif aunt_chars[char] == characteristics[char]:
            contains += 1

    return contains == 3

for aunt_sue in aunt_sues:
    contains = 0

    for char in characteristics:
        if char in aunt_sue['characteristics'] and aunt_sue['characteristics'][char] == characteristics[char]:
            contains += 1

    if contains == 3:
        print('P1:', aunt_sue['sue'])

    if comparator(aunt_sue['characteristics']):
        print('P2:', aunt_sue['sue'])

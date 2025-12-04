#!/usr/bin/env python3
import re


pattern = r'^(:?\d{1,})\1$'
pattern2 = r'^(:?\d{1,})\1+$'

ranges = [range(int(s[0]), int(s[1]) + 1) for s in [s.split('-') for s in open('./input.txt', 'r').read().split(',')]]

invalid = []

for rng in ranges:
    for n in rng:
        if len(str(n)) % 2 != 0:
            continue

        if re.match(pattern, str(n)):
            invalid.append(n)

p1 = sum(invalid)

print(f'P1: {p1}')

invalid = []

for rng in ranges:
    for n in rng:
        if re.match(pattern2, str(n)):
            invalid.append(n)

p2 = sum(invalid)

print(f'P2: {p2}')

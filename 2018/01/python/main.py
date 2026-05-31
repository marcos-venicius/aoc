#!/usr/bin/env python3

import re

file = './input.txt'

data = [x for x in re.split(r'\n|\s|,', open(file, 'r').read()) if x != '']

part_one = 0

for freq in data:
    if freq[0] == '+':
        part_one += int(freq[1:])
    elif freq[0] == '-':
        part_one -= int(freq[1:])
    else:
        raise Exception(f"invalid {freq}")

print(f'P1: {part_one}')

acc = 0
seen = set()
part_two = 0

while part_two == 0:
    for freq in data:
        if freq[0] == '+':
            acc += int(freq[1:])
        elif freq[0] == '-':
            acc -= int(freq[1:])
        else:
            raise Exception(f"invalid {freq}")

        if acc in seen:
            part_two = acc
            break

        seen.add(acc)

print(f'P2: {part_two}')

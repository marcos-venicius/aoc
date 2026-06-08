#!/usr/bin/env python3

import re


file = './input.txt'

data = [line for line in re.split(r'\s', open(file, 'r').read()) if line.strip() != '']


def count_letters(string):
    count = {}

    for l in string:
        if l not in count:
            count[l] = 0

        count[l] += 1

    exactly_three = 1 if sum([1 for x in count if count[x] == 3]) > 0 else 0
    exactly_two = 1 if sum([1 for x in count if count[x] == 2]) > 0 else 0

    return (exactly_three, exactly_two)

part_one = [ans for ans in [count_letters(line) for line in data] if ans[0] + ans[1] > 0]

exactly_three = sum([x[0] for x in part_one])
exactly_two = sum([x[1] for x in part_one])

part_one = exactly_two * exactly_three

print(f'P1: {part_one}')

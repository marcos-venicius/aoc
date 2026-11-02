#!/usr/bin/env python3

import re

INPUT = './input.txt'

data = list(filter(lambda x: x != '', re.split(r'\s', open(INPUT, 'r').read())))

freq = [{} for _ in range(len(data[0]))]

for line in data:
    for idx, char in enumerate(line):
        if char not in freq[idx]:
            freq[idx][char] = 1
        else:
            freq[idx][char] += 1

message = ''.join([sorted([(k, v) for k, v in table.items()], key=lambda x: x[1], reverse=True)[0][0] for table in freq])

print('P1:', message)

#!/usr/bin/env python3

import re

INPUT = './input.txt'

data = re.sub(r'\s', '', open(INPUT, 'r').read())

offset              = 0
size                = len(data)
decompressed_length = 0

def parse_marker():
    cursor = offset

    cursor += 1 # skip '('

    bot = cursor

    # consume length
    while data[cursor].isnumeric():
        cursor += 1

    length = int(data[bot:cursor])

    cursor += 1 # skip 'x'

    bot = cursor

    # consume repeat
    while data[cursor].isnumeric():
        cursor += 1

    repeat = int(data[bot:cursor])

    cursor += 1 # skip ')'
    
    return (cursor, length, repeat)

while offset < size:
    if data[offset] == '(':
        post_marker_offset, length, repeat = parse_marker()

        decompressed_length += length * repeat

        offset = post_marker_offset + length
    else:
        decompressed_length += 1

        offset += 1

print('P1:', decompressed_length)
print('P2:', None)

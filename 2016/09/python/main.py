#!/usr/bin/env python3

import re

INPUT = './input.txt'

data = re.sub(r'\s', '', open(INPUT, 'r').read())

global_offset                = 0
size                         = len(data)
decompressed_length_part_one = 0

def parse_marker(custom_offset=None):
    cursor = custom_offset if custom_offset is not None else global_offset

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

while global_offset < size:
    if data[global_offset] == '(':
        post_marker_offset, length, repeat = parse_marker()

        decompressed_length_part_one += length * repeat

        global_offset = post_marker_offset + length
    else:
        decompressed_length_part_one += 1

        global_offset += 1

def recursive_count(start, end, n):
    acc = 0
    cursor = start

    while cursor < end:
        if data[cursor] == '(':
            post_marker_offset, length, repeat = parse_marker(cursor)

            acc += recursive_count(post_marker_offset, post_marker_offset + length, repeat)

            cursor = post_marker_offset + length
        else:
            acc += 1
            cursor += 1

    return acc * n

decompressed_length_part_two = recursive_count(0, size, 1)

print('P1:', decompressed_length_part_one)
print('P2:', decompressed_length_part_two)

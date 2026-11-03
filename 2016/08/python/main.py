#!/usr/bin/env python3

TESTING = False

if TESTING:
    INPUT = './test.txt'
    M_W = 7
    M_H = 3
else:
    INPUT = './input.txt'
    M_W = 50
    M_H = 6

M = [[0 for _ in range(M_W)] for _ in range(M_H)]

class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __str__(self):
        return f'<rect w={self.w} h={self.h} />'

class Rotate:
    def __init__(self, orientation, coord, origin, destination):
        self.orientation = orientation
        self.coord = coord
        self.origin = origin
        self.destination = destination

    def __str__(self):
        return f'<rotate orientation={self.orientation} coord={self.coord} origin={self.origin} destination={self.destination} />'

def parse_row(row):
    offset = 0

    is_empty = lambda: offset >= len(row)

    while row[offset] != ' ':
        offset += 1

    command = row[:offset]

    offset += 1 # skip whitespace

    if command == 'rect':
        bot = offset

        while row[offset].isnumeric():
            offset += 1

        width = int(row[bot:offset])

        offset += 1 # skip 'x'

        bot = offset

        while not is_empty() and row[offset].isnumeric():
            offset += 1

        height = int(row[bot:offset])

        return Rect(width, height)
    elif command == 'rotate':
        bot = offset

        while row[offset] != ' ':
            offset += 1

        orientation = row[bot:offset]

        offset += 1 # skip whitespace

        coord = row[offset]

        offset += 1 # skip 'x/y'
        offset += 1 # skip '='

        bot = offset

        while row[offset].isnumeric():
            offset += 1

        origin = int(row[bot:offset])

        offset += 1 # skip whitespace

        # skip 'by'
        while row[offset] != ' ':
            offset += 1

        offset += 1 # skip whitespace

        bot = offset

        while not is_empty() and row[offset].isnumeric():
            offset += 1

        destination = int(row[bot:offset])

        return Rotate(orientation, coord, origin, destination)
    else:
        raise Exception(f'unrecognized command "{command}"')

def apply_rect_to_matrix(rect):
    for y in range(rect.h):
        for x in range(rect.w):
            M[y][x] = 1

def apply_rotate_to_matrix(rotate):
    if rotate.orientation == 'column':
        for _ in range(rotate.destination):
            pending = M[0][rotate.origin]
            next = None

            for y in range(1, len(M)):
                next = M[y][rotate.origin]
                M[y][rotate.origin] = pending
                pending = next

            M[0][rotate.origin] = pending
    elif rotate.orientation == 'row':
        for _ in range(rotate.destination):
            pending = M[rotate.origin][0]
            next = None

            for x in range(1, len(M[0])):
                next = M[rotate.origin][x]
                M[rotate.origin][x] = pending
                pending = next

            M[rotate.origin][0] = pending
    else:
        raise Exception(f'invalid orientation "{rotate.orientation}"')


rows = list(map(parse_row, list(filter(lambda x: x != '', open(INPUT, 'r').read().split('\n')))))

for row in rows:
    if isinstance(row, Rect):
        apply_rect_to_matrix(row)
    elif isinstance(row, Rotate):
        apply_rotate_to_matrix(row)
    else:
        raise Exception('invalid object')

part_one = sum([sum(row) for row in M])

print('P1:', part_one)

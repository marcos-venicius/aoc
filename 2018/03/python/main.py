#!/usr/bin/env python3

import sys
import re

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

class Claim:
    def __init__(self, tokens):
        self.claimId = int(tokens[0])
        self.x = int(tokens[1])
        self.y = int(tokens[2])
        self.w = int(tokens[3])
        self.h = int(tokens[4])

    def __str__(self):
        return f'<#{self.claimId} @ {self.x},{self.y}: {self.w}x{self.h}>'

    def __repr__(self):
        return self.__str__()

def parse_line(line):
    tokens = re.findall(r'\d+', line)

    return Claim(tokens)

claims: list[Claim] = [parse_line(line) for line in open(INPUT, 'r').read().strip().split('\n')]

def part_one():
    max_width = 0
    max_height = 0

    for claim in claims:
        max_width = max(claim.x + claim.w, max_width)
        max_height = max(claim.y + claim.h, max_height)

    board = [[0 for _ in range(max_width)] for _ in range(max_height)]

    answer = 0

    for claim in claims:
        for y in range(claim.y, claim.y + claim.h):
            for x in range(claim.x, claim.x + claim.w):
                board[y][x] += 1

    for row in board:
        for col in row:
            if col >= 2:
                answer += 1

    return answer


print('P1:', part_one())
print('P2:', None)

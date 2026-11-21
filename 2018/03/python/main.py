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

class OverlapCheckDispatcher:
    def __init__(self, claim, source, id):
        self.claim = claim
        self.source = source
        self.last_index_checked = -1
        self.elegible = True
        self.id = id

    def dispatch(self):
        if not self.elegible:
            return

        for i in range(self.last_index_checked + 1, len(self.source)):
            if self.id == i:
                continue

            self.last_index_checked = i

            if self.check_overlap(self.source[i]):
                self.elegible = False
                return

    def check_overlap(self, overlap: OverlapCheckDispatcher):
        a = self.claim
        b = overlap.claim

        return not (
            a.x + a.w <= b.x or
            b.x + b.w <= a.x or
            a.y + a.h <= b.y or
            b.y + b.h <= a.y
        )


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

def part_two():
    source = []

    source.append(OverlapCheckDispatcher(claims[0], source, 0))

    for i in range(1, len(claims)):
        source.append(OverlapCheckDispatcher(claims[i], source, i))

        for s in source:
            s.dispatch()

    elegible_id = None

    for overlap in source:
        if overlap.elegible:
            elegible_id = overlap.claim.claimId
            break

    return elegible_id

print('P1:', part_one())
print('P2:', part_two())

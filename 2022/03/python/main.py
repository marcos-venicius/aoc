#!/usr/bin/env python3

import re

INPUT = './test.txt' if (TEST := False) else './input.txt'

data = [(rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]) for rucksack in re.split(r'\s', open(INPUT, 'r').read().strip())]

def find_rucksacks_sharing_items(rucksack):
    left, right = rucksack

    for c1 in left:
        for c2 in right:
            if c1 == c2:
                return c1

    return None

def get_priority(type):
    ot = ord(type)
    oa = ord('a')
    oz = ord('z')
    oA = ord('A')

    if ot >= oa and ot <= oz:
        return ot - oa + 1

    return ot - oA + 27

part_one = sum([get_priority(find_rucksacks_sharing_items(rucksack)) for rucksack in data])

print('P1:', part_one)
#!/usr/bin/env python3

import re

INPUT = './test.txt' if (TEST := False) else './input.txt'

data = re.split(r'\s', open(INPUT, 'r').read().strip())
rucksacks = [(rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]) for rucksack in data]

elf_groups = [data[i:i+3] for i in range(0, len(data), 3)]

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

def get_common_between_groups(groups):
    count = [set() for _ in range(len(groups))]

    for i, group in enumerate(groups):
        for c in group:
            count[i].add(c)

    cross_data = {}

    for group_count in count:
        for key in group_count:
            cross_data[key] = cross_data.get(key, 0) + 1

    for key in cross_data:
        if cross_data[key] == len(groups):
            return key

    return None


part_one = sum([get_priority(find_rucksacks_sharing_items(rucksack)) for rucksack in rucksacks])
part_two = sum([get_priority(get_common_between_groups(groups)) for groups in elf_groups])

print('P1:', part_one)
print('P2:', part_two)

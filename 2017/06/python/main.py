#!/usr/bin/env python3

import re


def reallocate_banks_in_place(banks):
    argmax_bank = None

    for i in range(len(banks)):
        if argmax_bank is None or banks[i] > banks[argmax_bank]:
            argmax_bank = i

    blocks = banks[argmax_bank]

    banks[argmax_bank] = 0

    index = (argmax_bank + 1) % len(banks)

    while blocks > 0:
        banks[index] += 1

        blocks -= 1
        index = (index + 1) % len(banks)


def get_cache_key(banks):
    return ','.join(map(str, banks))


TEST = False
INPUT = 'test.txt' if TEST else 'input.txt'


data = list(map(int, re.split(r'\s', open(INPUT, 'r').read().strip())))


seen_before = set()
cycles = 0
part_one = None
part_two = None


while True:
    key = get_cache_key(data)

    if key in seen_before:
        if part_one is None:
            part_one = (cycles, key)
            cycles = 0
        elif part_one[1] == key:
            part_one = part_one[0]
            part_two = cycles
            break
    else:
        seen_before.add(key)

    reallocate_banks_in_place(data)
    cycles += 1


print('P1:', part_one)
print('P2:', part_two)


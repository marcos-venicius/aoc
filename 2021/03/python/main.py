#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

binary = [[c for c in line] for line in open(INPUT, 'r').read().strip().split('\n')]

def get_bits_count(base):
    bits = [{} for _ in range(len(base[0]))]

    for row in base:
        for i, v in enumerate(row):
            bits[i][v] = bits[i].get(v, 0) + 1

    return bits

bits = get_bits_count(binary)

gamma_rate = int(''.join([max(bit.keys(), key=lambda key: bit[key]) for bit in bits]), 2)
epsilon_rate = int(''.join([min(bit.keys(), key=lambda key: bit[key]) for bit in bits]), 2)

part_one = gamma_rate * epsilon_rate

print('P1:', part_one)

current_ogr = binary
current_csr = binary

x = 0

def check_rating(rating, when_equal, binary_list):
    if len(binary_list) == 1:
        return binary_list

    count = get_bits_count(binary_list)[x]

    keys = sorted(count.keys(), key=lambda key: count[key])

    least_common = keys[0]
    most_common = keys[1]

    are_equal = count[most_common] == count[least_common]

    equality = { 'csr': least_common, 'ogr': most_common }

    out = []

    for bin in binary_list:
        if (bin[x] == equality[rating] if not are_equal else bin[x] == when_equal):
            out.append(bin)
    
    return out

while len(current_ogr) > 1 or len(current_csr) > 1:
    current_ogr = check_rating(rating='ogr', when_equal='1', binary_list=current_ogr)
    current_csr = check_rating(rating='csr', when_equal='0', binary_list=current_csr)

    x += 1

ogr = int(''.join(current_ogr[0]), 2)
csr = int(''.join(current_csr[0]), 2)

part_two = ogr * csr

print('P2:', part_two)

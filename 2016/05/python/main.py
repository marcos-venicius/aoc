#!/usr/bin/env python3

import hashlib, re

FILE = 'input.txt'
PASS_SIZE = 8

door = re.sub(r'\s', '', open(FILE, 'r').read()).encode('utf-8')
base = hashlib.md5(door)

index = -1
part_one = []
part_two = [0] * PASS_SIZE
part_two_indexes = set()

while True:
    index += 1

    need_part_one = len(part_one) < PASS_SIZE
    need_part_two = len(part_two_indexes) < PASS_SIZE

    if not need_part_one and not need_part_two:
        break

    h = base.copy()
    h.update(b'%d' % index)
    d = h.digest()

    if d[0] or d[1] or d[2] > 0x0f:
        continue

    sixth, seventh = d[2], d[3] >> 4

    if need_part_one:
        part_one.append(f'{sixth:x}')

    if need_part_two:
        if sixth < len(part_two) and sixth not in part_two_indexes:
            part_two[sixth] = f'{seventh:x}'
            part_two_indexes.add(sixth)

print('P1:', ''.join(part_one))
print('P2:', ''.join(part_two))

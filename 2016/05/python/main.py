#!/usr/bin/env python3

import hashlib, re

FILE = 'input.txt'
PASS_SIZE = 8

password = re.sub(r'\s', '', open(FILE, 'r').read())

index = 0
part_one = []
part_two = [0] * PASS_SIZE
part_two_indexes = set()

while True:
    need_part_one = len(part_one) < PASS_SIZE
    need_part_two = len(part_two_indexes) < PASS_SIZE

    if not need_part_one and not need_part_two:
        break
    
    content = f'{password}{index}'

    hash = hashlib.md5(content.encode('utf-8')).hexdigest()

    if hash.startswith('00000'):
        if need_part_one:
            part_one.append(hash[5])

        if need_part_two:
            pos = int(hash[5]) if hash[5].isnumeric() else len(part_two)

            if pos < len(part_two) and pos not in part_two_indexes:
                part_two[pos] = hash[6]
                part_two_indexes.add(pos)

    index += 1

print('P1:', ''.join(part_one))
print('P2:', ''.join(part_two))

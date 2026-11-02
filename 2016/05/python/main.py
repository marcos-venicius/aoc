#!/usr/bin/env python3

import hashlib, re

FILE = 'input.txt'

password = re.sub(r'\s', '', open(FILE, 'r').read())

index = 0
chars = []

while len(chars) < 8:
    content = f'{password}{index}'

    hash = hashlib.md5(content.encode('utf-8')).hexdigest()

    if hash.startswith('00000'):
        chars.append(hash[5])

    index += 1

print(''.join(chars))

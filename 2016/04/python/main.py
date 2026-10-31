#!/usr/bin/env python3

import re
from collections import Counter

def parse(line):
  g = re.search(r'([a-z-]+)-(\d+)\[([a-z]+)\]', line)

  return (g.group(1), int(g.group(2)), g.group(3))

def is_real(name, checksum):
  count = {}

  for l in name.replace('-', ''):
    if l not in count:
      count[l] = 0

    count[l] += 1

  res = ''.join(sorted(count, key=lambda l: (-count[l], l))[:5])

  return res == checksum

file = './input.txt'

lines = open(file, 'r').read().split()

rooms = [parse(line) for line in lines]

print('P1:', sum(sector for name, sector, checksum in rooms if is_real(name, checksum)))

START = ord('a') - 1
Z = ord('z')

def decipher(text, offset):
  out = []

  for l in text:
    if l == '-':
      out.append(' ')
    else:
      idx = START + (((26 - (Z - ord(l))) + offset) % 26)

      out.append(chr(idx))

  return ''.join(out)

for name, sector, _ in rooms:
  decrypted = decipher(name, sector)

  if 'pole' in decrypted:
    print('P2:', sector)
    break

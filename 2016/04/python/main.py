#!/usr/bin/env python3

import re

file = './input.txt'

def decode_room_id(room):
  g = re.match(r'^((?:[a-z]+-)+)(\d+)\[([a-z]{5})\]$', room)

  name = g.group(1).replace('-', '')
  sector = int(g.group(2))
  checksum = [c for c in g.group(3)]

  by_letter = {}

  for i in range(len(name)):
    l = name[i]

    if l not in by_letter:
      by_letter[l] = (i, 1)
    else:
      by_letter[l] = (by_letter[l][0], by_letter[l][1] + 1)

  order = sorted([(k, by_letter[k][0], by_letter[k][1]) for k in by_letter], key=lambda x: x[-1], reverse=True)

  by_frequency = {}

  for k in by_letter:
    freq = by_letter[k][-1]

    if freq in by_frequency:
      by_frequency[freq].append((k, by_letter[k][0]))
    else:
      by_frequency[freq] = [(k, by_letter[k][0])]

  index = 0

  eq = lambda a,b: sum([ord(a[i][0]) - ord(b[i][0]) for i in range(len(a))]) == 0

  for i in range(len(checksum)):
    c = checksum[i]

    if c not in by_letter:
      return None

    freq = by_letter[c][-1]

    if len(by_frequency[freq]) == 1:
      if order[index][0] != c:
        return None
      index += 1
    elif not eq(sorted(by_frequency[freq], key=lambda x: x[0]), sorted(by_frequency[freq], key=lambda x: x[1])):
      return None

  return sector

data = [x for x in re.split(r'\s|\n', open(file, 'r').read()) if x != '']
part_one = sum([x for x in [decode_room_id(x) for x in data] if x is not None])

print(f'P1: {part_one}')



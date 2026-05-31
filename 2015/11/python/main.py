#!/usr/bin/env python3

from time import sleep

blocked = set(map(ord, ['i', 'o', 'l']))

min_c = ord('a')
max_c = ord('z')
data = [ord(c) for c in open('./test.txt', 'r').read().split('\n')[0]]

def increment_password(pos):
  if data[pos] == max_c:
    data[pos] = min_c
    for i in range(pos, len(data)):
      data[i] = min_c
    increment_password(pos - 1)
  else:
    data[pos] = data[pos] + 1

  for i in range(len(data)):
    if data[i] in blocked:
      increment_password(i)
      break

def print_password():
  print(''.join(map(chr, data)))

def is_valid_password():
  match_triplets = False
  pairs = 0

  for i in range(len(data)):
    if data[i] in blocked:
      return False

    if not (i + 2 >= len(data)):
      a = data[i]
      b = data[i + 1]
      c = data[i + 2]

      if b - a == 1 and c - b == 1:
        match_triplets = True

    if i >= len(data) - 1:
      continue

    has_prev = i - 1 >= 0

    if (has_prev and data[i] == data[i + 1] and data[i - 1] != data[i]):
      pairs += 1

  return pairs >= 2 and match_triplets

while not is_valid_password():
  increment_password(len(data) - 1)

print('P1: ', end='')
print_password()

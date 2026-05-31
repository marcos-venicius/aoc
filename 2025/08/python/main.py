#!/usr/bin/env python3

import math


## Test
#file = './test.txt'
#X = 10
# Input
file = './input.txt'
X = 1000

lines = [tuple(map(int, line.split(','))) for line in open(file, 'r').read().split('\n') if line.strip() != '']


distances = []

def calc_distance(p, q):
  return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)

for i in range(len(lines)):
  for j in range(i + 1, len(lines)):
    d = calc_distance(lines[i], lines[j])
    distances.append((d, i, j))

distances.sort(key=lambda x: x[0])


closest = distances[:X]

parent = list(range(len(lines)))
circuit_size = [1] * len(lines)

def find(i):
  if parent[i] == i:
    return i
  parent[i] = find(parent[i])
  return parent[i]

def union(i, j):
  root_i = find(i)
  root_j = find(j)

  if root_i != root_j:
    if circuit_size[root_i] < circuit_size[root_j]:
      root_i, root_j = root_j, root_i
    parent[root_j] = root_i
    circuit_size[root_i] += circuit_size[root_j]
    circuit_size[root_j] = 0

for d, u, v in closest:
  union(u, v)

final = sorted([size for size in circuit_size if size > 0], reverse=True)[:3]

part_one = final[0] * final[1] * final[2]

print(f'P1: {part_one}')

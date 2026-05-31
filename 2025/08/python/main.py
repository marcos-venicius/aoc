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
    distances.append((d, i, j, lines[i][0], lines[j][0]))

distances.sort(key=lambda x: x[0])


closest = distances[:X]

parent = list(range(len(lines)))
circuit_size = [1] * len(lines)
amount_of_circuits = len(circuit_size)
part_one = None
part_two = None

def find(i):
  if parent[i] == i: # is its own root
    return i
  parent[i] = find(parent[i]) # path compression, climb the tree to the upper most parent
  return parent[i]

def union(i, j):
  global amount_of_circuits, part_two

  root_i = find(i)
  root_j = find(j)

  if root_i != root_j:
    # union by size
    if circuit_size[root_i] < circuit_size[root_j]:
      root_i, root_j = root_j, root_i
    parent[root_j] = root_i
    circuit_size[root_i] += circuit_size[root_j]
    circuit_size[root_j] = 0
    amount_of_circuits -= 1

    # the first two points that led to a single circuit
    if amount_of_circuits == 1 and part_two is None:
      part_two = lines[i][0] * lines[j][0]

for d, u, v, _, _ in closest:
  union(u, v)

final = sorted([size for size in circuit_size if size > 0], reverse=True)[:3]

part_one = final[0] * final[1] * final[2]

print(f'P1: {part_one}')

# keep making union from where it stopped until the end
for d, u, v, _, _ in distances[X:]:
  union(u, v)

print(f'P2: {part_two}')

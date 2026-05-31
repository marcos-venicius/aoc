#!/usr/bin/env python3

file = './input.txt'

instructions = [line.split('\n')[0] for line in open(file, 'r').readlines()]

keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# starts at button "5"
x = 1
y = 1
M = { 'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0) }

def move(movement):
    global x, y

    m = M[movement]

    nx = x + m[0]
    ny = y + m[1]

    if ny >= 0 and ny < len(keypad) and nx >= 0 and nx < len(keypad[ny]):
        x = nx
        y = ny

code = []

for instruction_set in instructions:
    for movement in instruction_set:
        move(movement)

    code.append(keypad[y][x])

part_one = ''.join(map(str, code))

print(f'P1: {part_one}')

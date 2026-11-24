#!/usr/bin/env python3

import sys

INPUT = './test.txt' if (TEST := 'run' not in sys.argv) else './input.txt'

board = open(INPUT, 'r').read().strip().split('\n')

W, H = len(board[0]), len(board)

def run_slopes_logic(DX=3, DY=1):
    x, y = 0, 0
    counter = 0

    while True:
        nx = (x + DX) % W # right DX wrap at the end because the board keeps repeating
                          # in its width indefinitely so the next col when it finishes
                          # is always the first which began the board.
        ny = y + DY       # down DY

        # <> is it inside the board?

        if ny >= H: # only the y because we don't care about the x
            break

        x = nx
        y = ny

        if board[y][x] == '#':
            counter += 1

    return counter

part_one = run_slopes_logic()

tree_counts = [run_slopes_logic(dx, dy) for dx, dy in [(1, 1), (5, 1), (7, 1), (1, 2)]]

part_two = part_one

for count in tree_counts:
    part_two *= count

print('P1:', part_one)
print('P2:', part_two)

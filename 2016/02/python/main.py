#!/usr/bin/env python3

file = './input.txt'

instructions = [line.split('\n')[0] for line in open(file, 'r').readlines()]

class PadController:
    def __init__(self, keypad, start=(0, 0)):
        self.x = start[0]
        self.y = start[1]
        self.keypad = keypad
        self.M = { 'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0) }

    def move(self, movement):
        m = self.M[movement]

        nx = self.x + m[0]
        ny = self.y + m[1]

        if ny >= 0 and ny < len(self.keypad) and nx >= 0 and nx < len(self.keypad[ny]):
            if self.keypad[ny][nx] is not None:
                self.x = nx
                self.y = ny

    def exec_instruction(self, instructions):
        code = []

        for instruction_set in instructions:
            for movement in instruction_set:
                self.move(movement)

            code.append(self.keypad[self.y][self.x])

        return ''.join(map(str, code))

part_one = PadController([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
], (1, 1))

print(f'P1: {part_one.exec_instruction(instructions)}')

part_two = PadController([
    [None, None, '1', None, None],
    [None, '2',  '3', '4',  None],
    ['5',  '6',  '7', '8',   '9'],
    [None, 'A',  'B', 'C',  None],
    [None, None, 'D', None, None]
], (0, 2))

print(f'P2: {part_two.exec_instruction(instructions)}')

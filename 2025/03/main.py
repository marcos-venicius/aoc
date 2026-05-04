#!/usr/bin/env python3

import sys

def read_input(filename):
    return [[int(y) for y in x] for x in open(filename).read().split('\n') if len(x) > 0]

data = []

if len(sys.argv) != 2:
    print('usage: ./main.py <input file>')
    exit(1)

data = read_input(sys.argv[1])

def get_max_line_combination(line):
    last = None

    for i in range(0, len(line) - 1, 1):
        for j in range(i + 1, len(line), 1):
            comb = int(f'{line[i]}{line[j]}')

            if last is None:
                last = comb
            elif last < comb:
                last = comb

    return last

def get_max_line_combination_version_two(line, B=2):
    size = len(line)

    indexes = sorted([(i, line[i]) for i in range(size)], key=lambda x: x[1])

    full = line[::]
    length = len(full)

    bigger_digit_before_required_length = 0

    for i in range(size):
        if size - i < B:
            break

        if full[i] > full[bigger_digit_before_required_length]:
            bigger_digit_before_required_length = i

    for i in range(bigger_digit_before_required_length):
        full[i] = -1
        length -= 1

    for i in range(len(indexes)):
        if indexes[i][0] < bigger_digit_before_required_length:
            continue

        if length == B:
            break

        full[indexes[i][0]] = -1
        length -= 1

    full = [str(x) for x in full if x != -1]

    number = ''.join(full)

    return int(number)

def part_one():
    return sum([get_max_line_combination_version_two(line) for line in data])

def part_two():
    return sum([get_max_line_combination_version_two(line, 12) for line in data])

part_one_answer = part_one()
part_two_answer = part_two()

print(f'P1: {part_one_answer}');
print(f'P2: {part_two_answer}');

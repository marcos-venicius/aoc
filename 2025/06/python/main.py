#!/usr/bin/env python3

input_filename = './input.txt'

lines = [[y for y in x.split(' ') if y != '' and y != '\n'] for x in open(input_filename, 'r').read().split('\n') if x != '']

numbers = lines[:-1]
operations = lines[-1]

result = list(map(int, numbers[0]))

for values in numbers[1:]:
    for i in range(len(values)):
        result[i] = ({
            '*': result[i] * int(values[i]),
            '+': result[i] + int(values[i])
        })[operations[i]]

part_one = sum(result)

print(f'P1: {part_one}')


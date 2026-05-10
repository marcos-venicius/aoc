#!/usr/bin/env python3

input_filename = './input.txt'

data = open(input_filename, 'r').read()
lines = [[y for y in x.split(' ') if y != '' and y != '\n'] for x in data.split('\n') if x != '']

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

lines = [x for x in data.split('\n') if x != '']
numbers_lines = lines[:-1]
operations_line = lines[-1]

breakpoints = [i for i in range(len(operations_line)) if operations_line[i] != ' ']

columns = []

for line in numbers_lines:
    split = []

    last = breakpoints[0]

    for breakpoint in breakpoints[1:]:
        split.append(line[last:breakpoint - 1])
        last = breakpoint

    split.append(line[last:])

    for i in range(len(split)):
        if i >= len(columns):
            columns.append([])

        columns[i].append(split[i])

def get_numbers_from_column(column):
    numbers = []

    for row in column:
        for i in range(len(row)):
            if i >= len(numbers):
                numbers.append('')

            numbers[i] = f'{numbers[i]}{row[i].strip()}'

    return list(map(int, numbers))

numbers = [get_numbers_from_column(column) for column in columns]

result = [values[0] for values in numbers]

for i in range(len(numbers)):
    for value in numbers[i][1:]:
        result[i] = ({
            '*': result[i] * value,
            '+': result[i] + value,
        })[operations[i]]

print(f'P2: {sum(result)}')

#!/usr/bin/env python3

lines = [line for line in open('./input.txt', 'r').read().split('\n') if line != '']

data = {}

for line in lines:
    chunks = line.split(' ')

    f = chunks[0]
    m = chunks[2]
    a = chunks[3]
    t = chunks[-1][:-1]

    if f not in data:
        data[f] = {}

    if m == 'gain':
        data[f][t] = int(a)
    elif m == 'lose':
        data[f][t] = -int(a)
    else:
        raise Exception(f'invalid "{m}"')

def get_table(curr=[], amount=0):
    if len(curr) == len(data):
        return amount + data[curr[0]][curr[-1]] + data[curr[-1]][curr[0]]

    best = None

    for key in data[curr[-1]]:
        if key in curr:
            continue

        r = get_table(curr + [key], amount + data[curr[-1]][key] + data[key][curr[-1]])

        if best is None or r > best:
            best = r

    return best

start = next(iter(data))

print('P1:', get_table([start]))

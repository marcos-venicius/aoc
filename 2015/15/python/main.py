#!/usr/bin/env python3

import re

def mul(rows):
    x = None

    for i in range(len(rows[0])):
        s = sum(row[i] for row in rows)

        if s <= 0:
            return 0

        x = s if x is None else x * s

    return x

def splits(total, n):
    if n == 1:
        yield [total]
        return
    for k in range(total + 1):
        for rest in splits(total - k, n - 1):
            yield [k] + rest

def parse_line(line):
    pattern = r'(\w+): (\w+) (-?\d+), (\w+) (-?\d+), (\w+) (-?\d+), (\w+) (-?\d+), (\w+) (-?\d+)'

    result = re.search(pattern, line)

    response = {
        'name': result.group(1),
        'props': {}
    }

    for i in range(2, 12, 2):
        response['props'][result.group(i)] = int(result.group(i + 1))

    return response

ingredients = [parse_line(line) for line in open('./input.txt', 'r').read().split('\n') if line != '']

results = []

for ingredient in ingredients:
    props = ingredient['props']

    cap = props['capacity']
    dur = props['durability']
    fla = props['flavor']
    tex = props['texture']
    cal = props['calories']

    results.append([[cap * i, dur * i, fla * i, tex * i, cal * i] for i in range(0, 101)])

m = None
n = None

for amounts in splits(100, len(results)):
    rows = [results[j][amounts[j]][:-1] for j in range(len(results))]

    r = mul(rows)
    c = sum([results[j][amounts[j]][-1] for j in range(len(results))])

    if m is None or r > m:
        m = r

    if c == 500 and (n is None or r > n):
        n = r

print('P1:', m)
print('P2:', n)
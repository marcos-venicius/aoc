#!/usr/bin/env python3

data = []

file = open('../input.txt').read()

row = []

for c in file:
    if c == '\n':
        data.append(row)
        row = []
    else:
        row.append(c)


def oob(a):
    x = a[0]
    y = a[1]

    return y < 0 or y >= len(data) or x < 0 or x >= len(data)


def ib(a):
    x = a[0]
    y = a[1]

    return data[y][x] == '#'


def np(a, d):
    return (a[0] + d[0], a[1] + d[1])


def ggp():
    for y, chars in enumerate(data):
        for x, c in enumerate(chars):
            if c == '^':
                return [x, y]


def chk(m):
    nm = {}

    for key, v in m.items():
        nm[v] = key

    for k in nm:
        if k >= 8:
            return True

    return False


def itWorks(g):
    i, m = 0, {}

    d = (0, -1)

    while i < len(data) ** 3:
        i += 1

        next = np(g, d)

        if oob(next):
            break

        if ib(next):
            m[next] = m.get(next, 0) + 1

            if chk(m):
                return True

            d = tr(d)
            i -= 1
        else:
            g = next

    return False


def tr(a):
    x = a[0]
    y = a[1]

    if x == 0 and y == -1:
        return (1, 0)
    elif x == 1 and y == 0:
        return (0, 1)
    elif x == 0 and y == 1:
        return (-1, 0)
    elif x == -1 and y == 0:
        return (0, -1)


count = 0
g = ggp()

for y, chars in enumerate(data):
    for x, c in enumerate(chars):
        if c == '#' or c == '^':
            continue

        data[y][x] = '#'

        if itWorks(g):
            count += 1

        data[y][x] = c


print(count)


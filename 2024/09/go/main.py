#!/usr/bin/env python3
d = [x for x in '00...111...2...333.44.5555.6666.777.888899']

swap = [(int(x.split(' ')[1]), int(x.split(' ')[3].split('(')[0])) for x in """swap 2 with 41(9)
swap 3 with 40(9)
swap 4 with 39(8)
swap 8 with 38(8)
swap 9 with 37(8)
swap 10 with 36(8)
swap 12 with 34(7)
swap 13 with 33(7)
swap 14 with 32(7)
swap 18 with 30(6)
swap 21 with 29(6)
swap 26 with 28(6)""".split('\n')]


def show(x, y):
    for i, n in enumerate(d):
        if i == x:
            print(f"\033[1;32m{n.ljust(3, ' ')}\033[0m", end='')
        elif i == y:
            print(f"\033[1;31m{n.ljust(3, ' ')}\033[0m", end='')
        else:
            print(n.ljust(3, ' '), end='')
    print()
    for i in range(len(d)):
        if i == y:
            print(f"\033[1;31m{str(i).ljust(3, ' ')}\033[0m", end='')
        elif i == x:
            print(f"\033[1;32m{str(i).ljust(3, ' ')}\033[0m", end='')
        else:
            print(str(i).ljust(3, ' '), end='')
    print()

    print()


show(-1, -1)

for x, y in swap:
    d[x], d[y] = d[y], d[x]
    show(x, y)

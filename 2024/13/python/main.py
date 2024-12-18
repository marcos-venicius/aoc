#!/usr/bin/env python3

class ClawMachine:
    def __init__(self, configs):
        self.ax = configs[0][0]
        self.ay = configs[0][1]
        self.bx = configs[1][0]
        self.by = configs[1][1]
        self.px = configs[2][0]
        self.py = configs[2][1]

    def increaseAxisBy(self, x: int):
        self.px += x
        self.py += x

        return self


def get_data(string: str):
    lines = string.splitlines(False)

    items = []
    item = []

    for line in lines:
        if len(line.strip()) == 0:
            continue

        if line[0] == 'B':
            x, y = line.split(':')[1].strip().split(',')

            x = int(x.split('+')[1].strip())
            y = int(y.split('+')[1].strip())

            item.append((x, y))
        else:
            x, y = line.split(':')[1].strip().split(',')
            x = int(x.split('=')[1].strip())
            y = int(y.split('=')[1].strip())

            item.append((x, y))

        if len(item) == 3:
            items.append(item)
            item = []

    return items


def solve_claw_machine(m: ClawMachine):
    ca = (m.px * m.by - m.py * m.bx) / (m.ax * m.by - m.ay * m.bx)
    cb = (m.px - m.ax * ca) / m.bx

    if ca % 1 == 0 and cb % 1 == 0:
        return int(ca * 3 + cb)


input = open('../input.txt', 'r').read()

ans1 = 0
ans2 = 0

for claw_machine in get_data(input):
    machine = ClawMachine(claw_machine)

    res1 = solve_claw_machine(machine)
    res2 = solve_claw_machine(machine.increaseAxisBy(10000000000000))

    if res1 is not None:
        ans1 += res1

    if res2 is not None:
        ans2 += res2

print('Part 01:', ans1)
print('Part 02:', ans2)

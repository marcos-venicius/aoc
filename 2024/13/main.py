def click(x, y, t):
    return x * t, y * t


def calc(bx: int, by: int, ax: int, ay: int, x: int, y: int):
    cost = None

    for i in range(101):
        for j in range(101):
            ar = click(ax, ay, i)
            br = click(bx, by, j)

            if ar[0] + br[0] == x and ar[1] + br[1] == y:
                if cost is None:
                    cost = i * 3 + j
                else:
                    cost = min(cost, i * 3 + j)

    return cost


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


if True:
    input = open('./input.txt', 'r').read()
else:
    input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

ans = 0

for buttonA, buttonB, prize in get_data(input):
    res = calc(buttonB[0], buttonB[1], buttonA[0], buttonA[1], prize[0], prize[1])

    if res is not None:
        ans += res

print('Part 01:', ans)

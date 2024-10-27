#!/usr/bin/env python3


with open('input.txt', 'r', encoding='utf-8') as f:
    lines = [x.replace('\n', '') for x in f.readlines()]
    f.close()


class Parser:
    def __init__(self, lines: list[str]):
        self.lines = lines

    def parse(self) -> list[str]:
        return self.lines


class Solve:
    def __init__(self, lines: list[str]):
        parser = Parser(lines)

        self.lines = parser.parse()

    def solve(self):
        print(self.lines)


if __name__ == '__main__':
    solve = Solve(lines)

    solve.solve()
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

    def scape(self, line: str, i: int) -> tuple[int, int]:
        if line[i] != '\\':
            return 1, i + 1

        if line[i + 1] == 'x':
            return 1, i + 4
        elif line[i + 1] == '"' or line[i + 1] == '\\':
            return 1, i + 2


    def solve(self) -> int:
        codeCount = 0
        charsCount = 0

        for line in lines:
            codeCount += len(line)

            i, line = 0, line[1:-1]

            while i < len(line):
                c, ni = self.scape(line, i)

                charsCount += c
                i = ni

        return codeCount - charsCount


if __name__ == '__main__':
    solve = Solve(lines)

    res = solve.solve()

    print(res)

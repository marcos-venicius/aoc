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

    def encode(self, char: str) -> int:
        if char == '"' or char == '\\':
            return 2

        return 1

    def solve(self) -> int:
        codeCount = 0
        charsCount = 0

        for line in lines:
            codeCount += len(line)

            for char in line:
                charsCount += self.encode(char)

        doubleQuotesCount = len(lines) * 2
        charsCount += doubleQuotesCount

        return charsCount - codeCount


if __name__ == '__main__':
    solve = Solve(lines)

    res = solve.solve()

    print(res)

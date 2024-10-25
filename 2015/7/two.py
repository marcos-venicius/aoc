#!/usr/bin/env python3


with open('input.txt', 'r', encoding='utf-8') as f:
    lines = [x.replace('\n', '') for x in f.readlines()]
    f.close()


ASSIGN_KIND = 0
AND_KIND = 1
OR_KIND = 2
LSHIFT_KIND = 3
RSHIFT_KIND = 4
NOT_KIND = 5
ASSIGN_VAR_KIND = 6


t = {
    'AND': AND_KIND,
    'OR': OR_KIND,
    'LSHIFT': LSHIFT_KIND,
    'RSHIFT': RSHIFT_KIND,
}

tt = {
    AND_KIND: '&',
    OR_KIND: '|',
    LSHIFT_KIND: '<<',
    RSHIFT_KIND: '>>',
}


class Instruction:
    def __init__(self, instruction: str):
        self.instruction = instruction

        self.__parse()

    def __parse(self):
        split = self.instruction.split(' ')

        if len(split) == 3:
            if split[0].isnumeric():
                self.kind = ASSIGN_KIND
                self.value = int(split[0])
            else:
                self.kind = ASSIGN_VAR_KIND
                self.var = split[0]
        elif len(split) == 4:
            self.kind = NOT_KIND
            self.var = split[1]
        elif split[1] == 'LSHIFT' or split[1] == 'RSHIFT':
            self.left = split[0]
            self.value = int(split[2])
            self.kind = t[split[1]]
        else:
            self.left = split[0]
            self.right = split[2]
            self.kind = t[split[1]]

        self.output = split[-1]

    def __str__(self) -> str:
        if self.kind == ASSIGN_KIND:
            return f'{self.output} = {self.value}'
        if self.kind == ASSIGN_VAR_KIND:
            return f'{self.output} = {self.var}'
        elif self.kind == NOT_KIND:
            return f'{self.output} = NOT {self.var}'
        elif self.kind == LSHIFT_KIND or self.kind == RSHIFT_KIND:
            return f'{self.output} = {self.left} {tt[self.kind]} {self.value}'
        else:
            return f'{self.output} = {self.left} {tt[self.kind]} {self.right}'

        return '<unknown>'


class Parser:
    def __init__(self, lines: list[str]):
        self.lines = lines

    def parse(self) -> list[Instruction]:
        return [Instruction(line) for line in self.lines]
        

class Solve:
    values = {}
    def __init__(self, instructions: list[Instruction]):
        self.operations = instructions

        self.instructions = {}

        for instruction in instructions:
            if instruction.output not in self.instructions:
                self.instructions[instruction.output] = []
            
            self.instructions[instruction.output].append(instruction)

    def parse(self, instruction: Instruction):
        if instruction.kind == ASSIGN_KIND:
            self.values[instruction.output] = instruction.value
        elif instruction.kind == ASSIGN_VAR_KIND:
            if instruction.var not in self.values:
                for required_instruction in self.instructions[instruction.var]:
                    self.parse(required_instruction)

            self.values[instruction.output] = self.values[instruction.var]
        elif instruction.kind == LSHIFT_KIND or instruction.kind == RSHIFT_KIND:
            if instruction.left not in self.values:
                for required_instruction in self.instructions[instruction.left]:
                    self.parse(required_instruction)

            leftValue = self.values[instruction.left]
            value = instruction.value

            if instruction.kind == LSHIFT_KIND:
                self.values[instruction.output] = leftValue << value
            else:
                self.values[instruction.output] = leftValue >> value
        elif instruction.kind == NOT_KIND:
            if instruction.var not in self.values:
                for required_instruction in self.instructions[instruction.var]:
                    self.parse(required_instruction)

            varValue = self.values[instruction.var]

            self.values[instruction.output] = ~varValue & 0xFFFF
        else:
            if instruction.left not in self.values:
                if instruction.left in self.instructions:
                    for required_instruction in self.instructions[instruction.left]:
                        self.parse(required_instruction)

                    leftValue = self.values[instruction.left]
                else:
                    leftValue = int(instruction.left)
            else:
                leftValue = self.values[instruction.left]

            if instruction.right not in self.values:
                if instruction.right in self.instructions:
                    for required_instruction in self.instructions[instruction.right]:
                        self.parse(required_instruction)
                    rightValue = self.values[instruction.right]
                else:
                    rightValue = int(instruction.right)
            else:
                rightValue = self.values[instruction.right]

            if instruction.kind == AND_KIND:
                self.values[instruction.output] = leftValue & rightValue
            elif instruction.kind == OR_KIND:
                self.values[instruction.output] = leftValue | rightValue

    def solve(self, var: str, over: str):
        for instruction in self.instructions[var]:
            self.parse(instruction)

        currentVarValue = self.values[var]

        self.values = {
            over: currentVarValue
        }

        for instruction in self.instructions[var]:
            self.parse(instruction)

        return self.values


if __name__ == '__main__':
    parser = Parser(lines)

    instructions = parser.parse()
    solve = Solve(instructions)

    var = 'a'
    over = 'b'

    res = solve.solve(var, over)

    print(res[var])

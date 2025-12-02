#!/usr/bin/env python3

class DialNumber:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class Dial:
    def __init__(self, startsAt=0):
        head = DialNumber(0)
        tail = DialNumber(1, head)
        head.next = tail
        self.reset = None

        for i in range(2, 100):
            curr = DialNumber(i, tail)
            tail.next = curr
            tail = curr

        tail.next = head
        head.prev = tail

        self.current = head

        if startsAt != 0:
            self.right(startsAt)
            self.reset = self.current

    def restore(self):
        self.current = self.reset

    def right(self, n=1):
        zeroHits = 0

        for i in range(n):
            self.current = self.current.next

            if self.current.value == 0:
                zeroHits += 1

        return zeroHits

    def left(self, n=1):
        zeroHits = 0

        for i in range(n):
            self.current = self.current.prev

            if self.current.value == 0:
                zeroHits += 1

        return zeroHits

    def value(self):
        return self.current.value


class DialCommandParser:
    def __init__(self, filename: str, dial: Dial):
        self.lines = open(filename, 'r').readlines()
        self.dial = dial

    def execute(self):
        turnsToZero = 0

        for line in self.lines:
            if line.startswith('L'):
                n = int(line[1:])

                self.dial.left(n)

            elif line.startswith('R'):
                n = int(line[1:])

                self.dial.right(n)
            else:
                raise Exception(f'invalid line "{line}"')

            if self.dial.value() == 0:
                turnsToZero += 1

        return turnsToZero

    def executeV2(self):
        turnsToZero = 0

        for line in self.lines:
            if line.startswith('L'):
                n = int(line[1:])

                turnsToZero += self.dial.left(n)
            elif line.startswith('R'):
                n = int(line[1:])

                turnsToZero += self.dial.right(n)
            else:
                raise Exception(f'invalid line "{line}"')

        return turnsToZero


dial = Dial(50)
dialCommandParser = DialCommandParser('./input.txt', dial)

turnsToZero = dialCommandParser.execute()

print(f'P1: {turnsToZero}')

dial.restore()

turnsToZero = dialCommandParser.executeV2()

print(f'P2: {turnsToZero}')

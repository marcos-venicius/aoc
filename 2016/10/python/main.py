#!/usr/bin/env python3

import re

TEST = False


if TEST:
    FILE = './test.txt'
    COMPARISON = (2, 5)
else:
    FILE = './input.txt'
    COMPARISON = (61, 17)
    BINS = (0, 1, 2)

class Bot:
    def __init__(self, give_bot_cb, give_bin_cb):
        self.values = []
        self.instructions = []
        self.give_bot_cb = give_bot_cb
        self.give_bin_cb = give_bin_cb

    def exec_instruction(self):
        data = self.instructions.pop(0)

        for key in data:
            for target in data[key]:
                cb_fn    = self.give_bin_cb if target == 'output' else self.give_bot_cb
                value_fn = self.__get_low if key == 'low' else self.__get_high

                cb_fn(value_fn(), data[key][target])

    def give_instruction(self, instruction):
        self.instructions.append(instruction)

        self.__exec()

    def give_value(self, value):
        self.values.append(value)

        self.__exec()

    def compare(self, comparison):
        if len(self.values) < 2:
            return False

        return comparison[0] in self.values and comparison[1] in self.values

    def __exec(self):
        if len(self.values) == 2 and len(self.instructions) > 0:
            self.exec_instruction()

    def __get_low(self):
        return min(self.values)

    def __get_high(self):
        return max(self.values)

    def __str__(self):
        return f'values: {self.values}, instructions: {len(self.instructions)}'

def parse_line(line):
    tokens = re.split(r'\s', line)

    size = len(tokens)
    curr = 0

    token = lambda: tokens[curr] if curr < size else None

    while curr < size:
        if token() == 'value':
            curr += 1 # skip 'value'

            value = int(token())

            curr += 1 # skip THE value
            curr += 1 # skip 'goes'
            curr += 1 # skip 'to'
            curr += 1 # skip 'bot'

            bot = int(token())

            curr += 1 # skip THE bot

            return ('value', (value, bot))
        elif token() == 'bot':
            transaction = {
                'instruction': {}
            }

            curr += 1 # skip 'bot'

            transaction['bot'] = int(token())

            curr += 1 # skip THE bot
            curr += 1 # skip 'gives'

            while True:
                value = token()

                transaction['instruction'][value] = {} # low/high

                curr += 1 # skip what it gives
                curr += 1 # skip 'to'

                target = token()

                curr += 1 # skip target

                transaction['instruction'][value][target] = int(token())

                curr += 1 # skip the target value

                if token() != 'and':
                    break

                curr += 1 # skip 'and'

            return ('transaction', transaction)
        else:
            raise Exception(f'unhandled token "{token()}"')

    raise Exception('what?')

lines = list(map(parse_line, filter(lambda x: x != '', open(FILE, 'r').read().split('\n'))))

bots = {}
bins = {}

def give_bot_cb(value, id):
    if id not in bots:
        bots[id] = Bot(give_bot_cb, give_bin_cb)

    bots[id].give_value(value)

def give_bin_cb(value, id):
    if id not in bins:
        bins[id] = []

    bins[id].append(value)

for operation, data in lines:
    if operation == 'value':
        if data[-1] not in bots:
            bots[data[-1]] = Bot(give_bot_cb, give_bin_cb)

        bots[data[-1]].give_value(data[0])
    elif operation == 'transaction':
        if data['bot'] not in bots:
            bots[data['bot']] = Bot(give_bot_cb, give_bin_cb)

        bots[data['bot']].give_instruction(data['instruction'])
    else:
        raise Exception(f'invalid operation "{operation}"')


for id in bots:
    if bots[id].compare(COMPARISON):
        print('P1:', id)
        break

if not TEST:
    r = 0

    for bin in BINS:
        for v in bins[bin]:
            if r == 0:
                r = v
            else:
                r *= v

    print('P2:', r)
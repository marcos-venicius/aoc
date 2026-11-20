#!/usr/bin/env python3

import re
from one import run_part_one
from two import run_part_two

INPUT = './test.txt' if (TEST := False) else './input.txt'

data = list(map(int, open(INPUT, 'r').read().strip().split(',')))

if not TEST:
    data[1] = 12
    data[2] = 2

run_part_one(data[::])
run_part_two(data[::])

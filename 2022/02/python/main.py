#!/usr/bin/env python3

import re

INPUT = './test.txt' if (TEST := False) else './input.txt'

MAP = {
    'A': 'Rock',
    'B': 'Paper',
    'C': 'Scissors',
    'X': 'Rock',
    'Y': 'Paper',
    'Z': 'Scissors',
}

OUTCOMES = {
    ('Paper', 'Rock'): 'win',
    ('Rock', 'Paper'): 'lost',
    ('Rock', 'Scissors'): 'win',
    ('Scissors', 'Rock'): 'lost',
    ('Scissors', 'Paper'): 'win',
    ('Paper', 'Scissors'): 'lost',
    ('Paper', 'Paper'): 'draw',
    ('Scissors', 'Scissors'): 'draw',
    ('Rock', 'Rock'): 'draw'
}

RESULT = {
    'Paper': {
        'win': 'Scissors',
        'lost': 'Rock',
        'draw': 'Paper'
    },
    'Rock': {
        'win': 'Paper',
        'lost': 'Scissors',
        'draw': 'Rock'
    },
    'Scissors': {
        'win': 'Rock',
        'lost': 'Paper',
        'draw': 'Scissors'
    }
}

PART_TWO_OUTCOMES = {
    'Rock': 'lost',
    'Paper': 'draw',
    'Scissors': 'win'
}

SHAPES = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3
}

POINTS = {
    'lost': 0,
    'draw': 3,
    'win': 6
}


data = [MAP[x] for x in re.split(r'\s', open(INPUT, 'r').read().strip())]
data = [data[i:i + 2] for i in range(0, len(data), 2)]

score_part_one = 0
score_part_two = 0

def get_round_outcome_part_one(left, right):
    outcome = OUTCOMES[(left, right)]

    return POINTS[outcome] + SHAPES[right]

def get_round_outcome_part_two(left, right):
    outcome = PART_TWO_OUTCOMES[right]

    return POINTS[outcome] + SHAPES[RESULT[left][outcome]]
    

for left, right in data:
    score_part_one += get_round_outcome_part_one(left, right)
    score_part_two += get_round_outcome_part_two(left, right)


print('P1:', score_part_one)
print('P2:', score_part_two)

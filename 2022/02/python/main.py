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
    ('Paper', 'Rock'): ('win', 'lost'),
    ('Rock', 'Paper'): ('lost', 'win'),
    ('Rock', 'Scissors'): ('win', 'lost'),
    ('Scissors', 'Rock'): ('lost', 'win'),
    ('Scissors', 'Paper'): ('win', 'lost'),
    ('Paper', 'Scissors'): ('lost', 'win'),
    ('Paper', 'Paper'): ('draw', 'draw'),
    ('Scissors', 'Scissors'): ('draw', 'draw'),
    ('Rock', 'Rock'): ('draw', 'draw')
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

me = 0
he = 0

def get_round_outcome(left, right):
    left_outcome, right_outcome = OUTCOMES[(left, right)]

    return (
        POINTS[left_outcome] + SHAPES[left],
        POINTS[right_outcome] + SHAPES[right]
    )

for left, right in data:
    left_outcome, right_outcome = get_round_outcome(left, right)

    he += left_outcome
    me += right_outcome

print('P1:', me)

# rock defeats scissors
# scissors defeats paper
# paper defeats rock
# both sides equal: draw
#
# The first column is what my opponent is going to play
#  A: Rock
#  B: Paper
#  C: Scissors
# 
# The second column is what I should play in response:
#  X: Rock
#  Y: Paper
#  Z: Scissors
#
# Shapes:
#  Rock: 1
#  Paper: 2
#  Scissors: 3
#
# Outcome:
#  Lost: 0
#  Draw: 3
#  Won: 6
#
# The score is the sum of each round score:
# The score for each round is the score of the selected shape plus the outcome of the round

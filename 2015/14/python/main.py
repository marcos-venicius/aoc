#!/usr/bin/env python3

running_mode = 'running'
resting_mode = 'resting'

class Reindeer():
    def __init__(self, name, vel, duration, rest):
        self.name = name
        self.vel = vel
        self.duration = duration
        self.rest = rest
        self.mode = running_mode
        self.traveled = 0
        self.running_for = 0
        self.resting_for = 0
        self.points = 0

    def __str__(self):
        return f'Reindeer(name="{self.name}", mode={self.mode}, traveled={self.traveled})'

    def run(self):
        if self.mode == running_mode:
            if self.running_for == self.duration:
                self.mode = resting_mode
                self.running_for = 0
                self.resting_for = 1
            else:
                self.traveled += self.vel
                self.running_for += 1
        elif self.mode == resting_mode:
            if self.resting_for == self.rest:
                self.mode = running_mode
                self.resting_for = 0
                self.running_for = 1
                self.traveled += self.vel
            else:
                self.resting_for += 1

    def give_point(self):
        self.points += 1


def read_input():
    with open('../input.txt') as f:
        lines = f.readlines()
        f.close()

    data = []

    for line in lines:
        chunks = line.split(' ')

        name = chunks[0]
        vel = int(chunks[3])
        duration = int(chunks[6])
        rest = int(chunks[13])
        reindeer = Reindeer(name, vel, duration, rest)

        data.append(reindeer)

    return data

seconds = 2503
reindeers = read_input()

for s in range(seconds):
    winners = []

    for reindeer in reindeers:
        reindeer.run()

        if len(winners) == 0 or reindeer.traveled == winners[0].traveled:
            winners.append(reindeer)
        elif reindeer.traveled > winners[0].traveled:
            winners = [reindeer]

    for winner in winners:
        winner.give_point()

winner_by_travel = reindeers[0]
winner_by_points = reindeers[0]

for reindeer in reindeers:
    if reindeer.traveled > winner_by_travel.traveled:
        winner_by_travel = reindeer

    if reindeer.points > winner_by_points.points:
        winner_by_points = reindeer

print('Part 01:', winner_by_travel.traveled)
print('Part 02:', winner_by_points.points)

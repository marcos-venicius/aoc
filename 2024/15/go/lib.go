package main

import (
	"fmt"
)

type Direction rune

type Warehouse struct {
	grid       [][]rune
	w, h       int
	robot      Vec2
	directions []Direction
}

const (
	TOP    Direction = '^'
	RIGHT  Direction = '>'
	BOTTOM Direction = 'v'
	LEFT   Direction = '<'
)

func CreateWarehouse() Warehouse {
	return Warehouse{
		grid:       make([][]rune, 0),
		robot:      Vec2{0, 0},
		w:          0,
		h:          0,
		directions: make([]Direction, 0),
	}
}

func (w Warehouse) at(v Vec2) rune {
	return w.grid[v.y][v.x]
}

func (w Warehouse) Display() {
	for _, row := range w.grid {
		for _, c := range row {
			if c == '@' {
				printf("\033[1;31m%c\033[0m", c)
			} else {
				printf("%c", c)
			}
		}
		println()
	}
	println()
}

func (w *Warehouse) ParseLine(line string) {
	if len(line) == 0 {
		return
	}

	translation := map[rune]Direction{
		'^': TOP,
		'>': RIGHT,
		'v': BOTTOM,
		'<': LEFT,
	}

	if line[0] == '#' {
		w.h++

		row := make([]rune, 0, len(line))

		for i, c := range line {
			row = append(row, c)

			if c == '@' {
				w.robot.x = i
				w.robot.y = len(w.grid)
			}
		}

		w.grid = append(w.grid, row)
		w.w = max(w.w, len(row))

		return
	}

	for _, c := range line {
		if d, ok := translation[c]; ok {
			w.directions = append(w.directions, d)
		} else {
			panic(fmt.Sprintf("invalid \"%c\" direction char", c))
		}
	}
}

func (w Warehouse) isInBounds(v Vec2) bool {
	return v.x >= 0 && v.x < w.w && v.y >= 0 && v.y < w.h
}

func (w Warehouse) isBlank(v Vec2) bool {
	if !w.isInBounds(v) {
		return false
	}

	return w.grid[v.y][v.x] == '.'
}

func (w Warehouse) isAWall(v Vec2) bool {
	if !w.isInBounds(v) {
		return false
	}

	return w.at(v) == '#'
}

func (w *Warehouse) Move(from Vec2, direction Direction) {
	directions := map[Direction]Vec2{
		TOP:    vec2(0, -1),
		RIGHT:  vec2(1, 0),
		BOTTOM: vec2(0, 1),
		LEFT:   vec2(-1, 0),
	}

	dir := directions[direction]

	to := from.Sum(dir)

	motions := make([]Vec2, 0, ternary(from.y, direction == TOP, ternary(w.h-from.y, direction == BOTTOM, ternary(from.x, direction == LEFT, w.w-from.x))))

	isPossibleToMove := true

	for {
		if w.isAWall(to) {
			isPossibleToMove = false
			break
		}

		motions = append(motions, to)

		if w.isBlank(to) {
			break
		}

		to = to.Sum(dir)
	}

	if !isPossibleToMove {
		return
	}

	for _, m := range motions {
		w.grid[m.y][m.x] = 'O'
	}

	nrp := w.robot.Sum(dir)

	w.grid[nrp.y][nrp.x] = '@'
	w.grid[from.y][from.x] = '.'

	w.robot = nrp
}

func (w Warehouse) SumBoxesCoordinates() int {
	sum := 0

	for y, row := range w.grid {
		for x, v := range row {
			if v == 'O' {
				sum += 100*y + x
			}
		}
	}

	return sum
}

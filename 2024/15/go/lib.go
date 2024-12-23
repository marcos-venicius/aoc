package main

import (
	"fmt"
)

type Movement rune

const (
	TOP    Movement = '^'
	RIGHT  Movement = '>'
	BOTTOM Movement = 'v'
	LEFT   Movement = '<'
)

type Vec2 struct {
	x, y int
}

type Warehouse struct {
	grid      [][]rune
	w, h      int
	robot     Vec2
	movements []Movement
}

func (v Vec2) Diff(of Vec2) Vec2 {
	return Vec2{
		x: of.x - v.x,
		y: of.y - v.y,
	}
}

func (v Vec2) Abs() Vec2 {
	out := Vec2{
		x: v.x,
		y: v.y,
	}

	if v.x < 0 {
		out.x = v.x * -1
	}

	if v.y < 0 {
		out.y = v.y * -1
	}

	return out
}

func (v Vec2) DecY(n int) Vec2 {
	return Vec2{
		x: v.x,
		y: v.y - n,
	}
}

func (v Vec2) IncY(n int) Vec2 {
	return Vec2{
		x: v.x,
		y: v.y + n,
	}
}

func (v Vec2) DecX(n int) Vec2 {
	return Vec2{
		x: v.x - n,
		y: v.y,
	}
}

func (v Vec2) IncX(n int) Vec2 {
	return Vec2{
		x: v.x + n,
		y: v.y,
	}
}

func CreateWarehouse() Warehouse {
	return Warehouse{
		grid:      make([][]rune, 0),
		robot:     Vec2{0, 0},
		w:         0,
		h:         0,
		movements: make([]Movement, 0),
	}
}

func (w Warehouse) at(v Vec2) rune {
	return w.grid[v.y][v.x]
}

func (w Warehouse) Display() {
	for _, row := range w.grid {
		for _, c := range row {
			if c == '@' {
				fmt.Printf("\033[1;31m%c\033[0m", c)
			} else {
				fmt.Printf("%c", c)
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
	} else {
		for _, c := range line {
			switch c {
			case '^':
				w.movements = append(w.movements, TOP)
				break
			case '>':
				w.movements = append(w.movements, RIGHT)
				break
			case 'v':
				w.movements = append(w.movements, BOTTOM)
				break
			case '<':
				w.movements = append(w.movements, LEFT)
				break
			default:
				panic(fmt.Sprintf("invalid \"%c\" direction char", c))
			}
		}
	}
}

func (w Warehouse) isInBounds(v Vec2) bool {
	return v.x >= 0 && v.x < w.w && v.y >= 0 && v.y < w.h
}

func (w Warehouse) isFree(v Vec2) bool {
	if !w.isInBounds(v) {
		return false
	}

	return w.grid[v.y][v.x] == '.'
}

func (w Warehouse) canMove(v Vec2) bool {
	if !w.isInBounds(v) {
		return false
	}

	switch w.at(v) {
	case 'O', '[', ']':
		return true
	}

	return false
}

func (w Warehouse) SumBoxesCoordinates() int {
	sum := 0

	for y, row := range w.grid {
		for x, v := range row {
			if v == 'O' || v == '[' {
				sum += 100*y + x
			}
		}
	}

	return sum
}

func (w *Warehouse) Move(from Vec2, movement Movement, updateRobot bool) bool {
	var to Vec2

	switch movement {
	case TOP:
		to = from.DecY(1)
		break
	case RIGHT:
		to = from.IncX(1)
		break
	case BOTTOM:
		to = from.IncY(1)
		break
	case LEFT:
		to = from.DecX(1)
		break
	default:
		panic("invalid movement")
	}

	if w.isFree(to) {
		w.grid[from.y][from.x], w.grid[to.y][to.x] = w.grid[to.y][to.x], w.grid[from.y][from.x]

		if updateRobot {
			w.robot = to
		}

		return true
	} else if w.canMove(to) {
		if w.Move(to, movement, false) {
			w.grid[from.y][from.x], w.grid[to.y][to.x] = w.grid[to.y][to.x], w.grid[from.y][from.x]

			if updateRobot {
				w.robot = to
			}

			return true
		}
	}

	return false
}

func (w *Warehouse) freePath(p Vec2, dir Movement) bool {
  if w.isFree(p) {
    return true
  }

	if dir != TOP && dir != BOTTOM {
		panic("invalid direction")
	}

	var left, right Vec2

	if w.at(p) == ']' {
		left = p.DecX(1)
		right = p
	} else if w.at(p) == '[' {
		left = p
		right = p.IncX(1)
	} else {
		return false
	}

	leftDir, rightDir := left.DecY(1), right.DecY(1)

	if dir == BOTTOM {
		leftDir, rightDir = left.IncY(1), right.IncY(1)
	}

	if !w.freePath(leftDir, dir) {
    return false
  }

	if !w.freePath(rightDir, dir) {
    return false
  }

	w.grid[left.y][left.x], w.grid[leftDir.y][leftDir.x] = w.grid[leftDir.y][leftDir.x], w.grid[left.y][left.x]
	w.grid[right.y][right.x], w.grid[rightDir.y][rightDir.x] = w.grid[rightDir.y][rightDir.x], w.grid[right.y][right.x]

	return true
}

func (w *Warehouse) MovePairs(from Vec2, movement Movement, updateRobot bool) bool {
	var to Vec2

	switch movement {
	case TOP:
		to = from.DecY(1)
		break
	case RIGHT:
		to = from.IncX(1)
		break
	case BOTTOM:
		to = from.IncY(1)
		break
	case LEFT:
		to = from.DecX(1)
		break
	default:
		panic("invalid movement")
	}

	if w.isFree(to) {
		w.grid[from.y][from.x], w.grid[to.y][to.x] = w.grid[to.y][to.x], w.grid[from.y][from.x]

		if updateRobot {
			w.robot = to
		}

		return true
	} else if w.canMove(to) {
		if movement == TOP || movement == BOTTOM {
			if !w.freePath(to, movement) {
				return false
			}
		} else if !w.MovePairs(to, movement, false) {
			return false
		}

		w.grid[from.y][from.x], w.grid[to.y][to.x] = w.grid[to.y][to.x], w.grid[from.y][from.x]

		if updateRobot {
			w.robot = to
		}

		return true
	}

	return false
}

func (w *Warehouse) GrowMap() {
	for i, row := range w.grid {
		out := make([]rune, 0)

		for _, c := range row {
			switch c {
			case '@':
				out = append(out, '@')
				out = append(out, '.')
				break
			case 'O':
				out = append(out, '[')
				out = append(out, ']')
				break
			default:
				out = append(out, c)
				out = append(out, c)
				break
			}
		}

		w.w = max(w.w, len(out))

		w.grid[i] = out
	}

	for y, row := range w.grid {
		for x, c := range row {
			if c == '@' {
				w.robot = Vec2{x: x, y: y}
				break
			}
		}
	}
}

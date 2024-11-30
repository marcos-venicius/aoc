package main

import (
	"regexp"
	"strconv"
)

type Direction int
type Vector2 struct{ x, y int }

type Instruction struct {
	direction Direction
	blocks    int
}

var Empty = struct{}{}

const (
	L Direction = iota
	R Direction = iota
)

var (
	N = Vector2{x: 0, y: -1}
	E = Vector2{x: 1, y: 0}
	S = Vector2{x: 0, y: 1}
	W = Vector2{x: -1, y: 0}
)

func abs(x int) int {
	if x < 0 {
		return x * -1
	}

	return x
}

func (v *Vector2) is(axis Vector2) bool {
	return v.x == axis.x && v.y == axis.y
}

func (v *Vector2) rotateLeft() Vector2 {
	switch *v {
	case N:
		return W
	case W:
		return S
	case S:
		return E
	case E:
		return N
	default:
		panic("Invalid left axis rotation")
	}
}

func (v *Vector2) rotateRight() Vector2 {
	switch *v {
	case N:
		return E
	case E:
		return S
	case S:
		return W
	case W:
		return N
	default:
		panic("Invalid right axis rotation")
	}
}

func parseLine(line string) []Instruction {
	regex := regexp.MustCompile("(R|L)(\\d+)")

	instructions := make([]Instruction, 0)

	matches := regex.FindAllStringSubmatch(line, -1)

	for _, match := range matches {
		direction := R

		if match[1] == "L" {
			direction = L
		}

		blocks, err := strconv.Atoi(match[2])

		if err != nil {
			panic(err)
		}

		instruction := Instruction{
			direction: direction,
			blocks:    blocks,
		}

		instructions = append(instructions, instruction)
	}

	return instructions
}

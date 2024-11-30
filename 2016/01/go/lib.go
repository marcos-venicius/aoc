package main

import (
	"regexp"
	"strconv"
)

type Direction int
type Axis struct{ x, y int }

type Instruction struct {
	direction Direction
	blocks    int
}

const (
	L Direction = iota
	R Direction = iota
)

var (
	N = Axis{x: 0, y: -1}
	E = Axis{x: 1, y: 0}
	S = Axis{x: 0, y: 1}
	W = Axis{x: -1, y: 0}
)

func (a *Axis) is(axis Axis) bool {
	return a.x == axis.x && a.y == axis.y
}

func (a *Axis) rotateLeft() Axis {
	switch *a {
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

func (a *Axis) rotateRight() Axis {
	switch *a {
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

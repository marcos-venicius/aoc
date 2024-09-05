package main

import (
	"log"
	"os"
	"strconv"
	"strings"
)

type LightAction = int

type Position struct {
	x int
	y int
}

type Line struct {
	action LightAction
	from   Position
	to     Position
}

type Matrix [][]int

const (
	turnLightOn  LightAction = iota
	turnLightOff LightAction = iota
	toggleLight  LightAction = iota
)

func readLines() []string {
	data, err := os.ReadFile("./input.txt")

	if err != nil {
		log.Fatal(err)
	}

	return strings.Split(string(data), "\n")
}

func initMatrix() Matrix {
	const size = 1000

	matrix := make(Matrix, size)

	for i := range matrix {
		matrix[i] = make([]int, size)
	}

	return matrix
}

func parseLine(line string) Line {
	split := strings.Split(line, " ")

	l := Line{}

	ts := strings.Split(split[len(split)-1], ",")
	tf, _ := strconv.Atoi(ts[0])
	tt, _ := strconv.Atoi(ts[1])

	l.to = Position{
		x: tf,
		y: tt,
	}

	if split[0] == "toggle" {
		l.action = toggleLight

		fs := strings.Split(split[1], ",")
		ff, _ := strconv.Atoi(fs[0])
		ft, _ := strconv.Atoi(fs[1])

		l.from = Position{
			x: ff,
			y: ft,
		}
	} else {
		fs := strings.Split(split[2], ",")
		ff, _ := strconv.Atoi(fs[0])
		ft, _ := strconv.Atoi(fs[1])

		l.from = Position{
			x: ff,
			y: ft,
		}
	}

	switch split[1] {
	case "on":
		l.action = turnLightOn
	case "off":
		l.action = turnLightOff
	}

	return l
}

func max(a, b int) int {
	if a > b {
		return a
	}

	return b
}

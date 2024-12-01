package main

import (
	"regexp"
	"strconv"
)

type Line struct {
	left  int
	right int
}

func parseLine(line string) Line {
	regex := regexp.MustCompile(`(\d+)\s*(\d+)`)

	list := regex.FindAllStringSubmatch(line, -1)

	left, err := strconv.Atoi(list[0][1])

	if err != nil {
		panic(err)
	}

	right, err := strconv.Atoi(list[0][2])

	if err != nil {
		panic(err)
	}

	return Line{
		left:  left,
		right: right,
	}
}

func abs(x int) int {
	if x < 0 {
		return x * -1
	}

	return x
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	input := parseInput(reader)

	height := len(input)
	width := len(input[0])

	antenas := make(map[rune][]Vector2)

	for y, row := range input {
		for x, char := range row {
			if char == '.' {
				continue
			}

			if _, ok := antenas[char]; !ok {
				antenas[char] = make([]Vector2, 0)
			}

			antenas[char] = append(antenas[char], Vector2{x: x, y: y})
		}
	}

	antinodes := make(map[Vector2]struct{})

	for _, array := range antenas {
		for i := 0; i < len(array); i++ {
			for j := i + 1; j < len(array); j++ {
				a := array[i]
				b := array[j]

				ant1 := Vector2{x: 2*a.x - b.x, y: 2*a.y - b.y}
				ant2 := Vector2{x: 2*b.x - a.x, y: 2*b.y - a.y}

				if !isOutOfBounds(ant1.x, ant1.y, width, height) {
					antinodes[ant1] = struct{}{}
				}

				if !isOutOfBounds(ant2.x, ant2.y, width, height) {
					antinodes[ant2] = struct{}{}
				}
			}
		}
	}

	ans := len(antinodes)

	fmt.Printf("01: %d\n", ans)

	return ans
}

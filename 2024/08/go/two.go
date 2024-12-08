package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
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
			for j := i; j < len(array); j++ {
				if j == i {
					continue
				}

				a := array[i]
				b := array[j]

				dx := b.x - a.x
				dy := b.y - a.y

				x1, y1 := a.x, a.y
				x2, y2 := a.x, a.y

				for {
					one := true
					two := true

					if !isOutOfBounds(x1, y1, width, height) {
						one = false

						antinodes[Vector2{x: x1, y: y1}] = struct{}{}

						x1 -= dx
						y1 -= dy
					}

					if !isOutOfBounds(x2, y2, width, height) {
						two = false

						antinodes[Vector2{x: x2, y: y2}] = struct{}{}

						x2 += dx
						y2 += dy
					}

					if one && two {
						break
					}
				}
			}
		}
	}

	ans := len(antinodes)

	fmt.Printf("02: %d\n", ans)

	return ans
}

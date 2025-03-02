package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0

outer:
	for reader.Running() {
		_, line := reader.Line()

		visited := make(map[Vector2]struct{})
		instructions := parseLine(line)

		direction := N

		pos := Vector2{}

		visited[pos] = Empty

		for _, i := range instructions {
			if i.direction == R {
				direction = direction.rotateRight()
			} else if i.direction == L {
				direction = direction.rotateLeft()
			} else {
				panic("Invalid rotation")
			}

			for d := 0; d < i.blocks; d++ {
				pos.x += direction.x
				pos.y += direction.y

				if _, ok := visited[pos]; ok {
					ans = abs(pos.x) + abs(pos.y)

					break outer
				}

				visited[pos] = Empty
			}
		}
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		_, line := reader.Line()

		instructions := parseLine(line)

		direction := N

		pos := Vector2{}

		for _, i := range instructions {
			if i.direction == R {
				direction = direction.rotateRight()
			} else if i.direction == L {
				direction = direction.rotateLeft()
			} else {
				panic("Invalid rotation")
			}

			pos.x += direction.x * i.blocks
			pos.y += direction.y * i.blocks
		}

		ans = abs(pos.x) + abs(pos.y)
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

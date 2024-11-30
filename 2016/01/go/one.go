package main

import (
	"fmt"
	"math"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	reader.Read(func(line string) bool {
		instructions := parseLine(line)

		direction := N

		x, y := 0, 0

		for _, i := range instructions {
			if i.direction == R {
				direction = direction.rotateRight()
			} else if i.direction == L {
				direction = direction.rotateLeft()
			} else {
				panic("Invalid rotation")
			}

			x += direction.x * i.blocks
			y += direction.y * i.blocks
		}

		ans = int(math.Abs(float64(x)) + math.Abs(float64(y)))

		return true
	})

	fmt.Printf("01: %d\n", ans)

	return ans
}

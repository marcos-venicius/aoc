package main

import (
	"fmt"
)

func solveTwo(input Input) int {
	ans := 0

	for y := 0; y < input.height; y++ {
		for x := 0; x < input.width; x++ {
			if input.findCrossWord(x, y) {
				ans++
			}
		}
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

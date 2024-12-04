package main

import (
	"fmt"
)

var (
	top         = [2]int{0, -1}
	topRight    = [2]int{1, -1}
	right       = [2]int{1, 0}
	bottomRight = [2]int{1, 1}
	bottom      = [2]int{0, 1}
	bottomLeft  = [2]int{-1, 1}
	left        = [2]int{-1, 0}
	topLeft     = [2]int{-1, -1}
)

func solveOne(input Input) int {
	ans := 0

	directions := [][2]int{
		top,
		topRight,
		right,
		bottomRight,
		bottom,
		bottomLeft,
		left,
		topLeft,
	}

	cache := make(map[string]struct{})

	for y := 0; y < input.height; y++ {
		for x := 0; x < input.width; x++ {
			for _, direction := range directions {
				wordFound := input.findWord(cache, x, y, direction[0], direction[1])

				if wordFound {
					ans++
				}
			}
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

package main

import (
	"fmt"
)

func solveTwo(lines []string) {
	ans := 0

	line := lines[0]

	var p string

	sx, sy, rx, ry, v := 0, 0, 0, 0, make(map[string]struct{})

	movements := map[rune][2]int{
		'^': {0, -1},
		'v': {0, 1},
		'>': {1, 0},
		'<': {-1, 0},
	}

	for index, m := range line {
		rm := index % 2

		if rm == 0 {
			rx += movements[m][0]
			ry += movements[m][1]
			p = fmt.Sprintf("%dx%d", rx, ry)
		} else {
			sx += movements[m][0]
			sy += movements[m][1]
			p = fmt.Sprintf("%dx%d", sx, sy)
		}

		_, ok := v[p]

		if !ok {
			ans++
		}

		v[p] = struct{}{}
	}

	fmt.Printf("02: %d\n", ans)
}

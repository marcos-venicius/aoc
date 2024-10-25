package main

import (
	"fmt"
)

func solveOne(lines []string) {
	ans := 0

	line := lines[0]

	x, y, v := 0, 0, make(map[string]struct{})

	for _, m := range line {
		p := fmt.Sprintf("%dx%d", x, y)

		if _, ok := v[p]; !ok {
			ans += 1
		}

		v[p] = struct{}{}

		switch m {
		case '^':
			y--
			break
		case 'v':
			y++
			break
		case '>':
			x++
			break
		case '<':
			x--
			break
		default:
			break
		}
	}

	fmt.Printf("01: %d\n", ans)
}

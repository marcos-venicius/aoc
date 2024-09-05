package main

import (
	"fmt"
)

func solveTwo(lines []string) int {
	brightness := 0

	m := initMatrix()

	for _, line := range lines {
		l := parseLine(line)

		for c := l.from.x; c <= l.to.x; c++ {
			for r := l.from.y; r <= l.to.y; r++ {
				switch l.action {
				case toggleLight:
					m[r][c] += 2

					brightness += 2
				case turnLightOn:
					m[r][c]++
					brightness++
				case turnLightOff:
					v := m[r][c] - 1

					m[r][c] = max(v, 0)

					if brightness > 0 && v >= 0 {
						brightness--
					}
				}
			}
		}
	}

	fmt.Printf("02: %d\n", brightness)

	return brightness
}

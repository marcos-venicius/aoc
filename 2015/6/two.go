package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	brightness := 0

	m := initMatrix()

	reader.Read(func(line string) bool {
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

		return false
	})

	fmt.Printf("02: %d\n", brightness)

	return brightness
}

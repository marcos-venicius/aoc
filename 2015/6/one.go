package main

import (
	"fmt"
)

func solveOne(reader LinesReader) int {
	m := initMatrix()

	litLights := 0

	reader.Read(func(line string) bool {
		l := parseLine(line)

		for c := l.from.x; c <= l.to.x; c++ {
			for r := l.from.y; r <= l.to.y; r++ {
				curr := m[r][c]

				switch l.action {
				case toggleLight:
					m[r][c] ^= 1
					if curr == 0 {
						litLights++
					} else {
						litLights--
					}
				case turnLightOn:
					m[r][c] = 1
					if curr == 0 {
						litLights++
					}
				case turnLightOff:
					m[r][c] = 0
					if curr == 1 {
						litLights--
					}
				}
			}
		}

		return false
	})

	fmt.Printf("01: %d\n", litLights)

	return litLights
}

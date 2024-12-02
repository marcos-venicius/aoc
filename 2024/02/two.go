package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		_, line := reader.Line()
		parsedLine := parseLine(line)

		if isSafe(parsedLine) {
			ans += 1
		} else {
			for i := 0; i < len(parsedLine); i++ {
				newline := []int{}
        newline = append(newline, parsedLine[:i]...)
				newline = append(newline, parsedLine[i+1:]...)

				if isSafe(newline) {
					ans += 1
					break
				}
			}
		}
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

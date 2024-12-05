package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		_, line := reader.Line()

		digits := parseLine(line)

		for i, d := range digits {
			next := (i + 1) % len(digits)

			if d == digits[next] {
				ans += d
			}
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

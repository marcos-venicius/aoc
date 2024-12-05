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
			if i == len(digits)-1 {
				if d == digits[0] {
					ans += d
				}
			} else if d == digits[i+1] {
				ans += d
			}
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

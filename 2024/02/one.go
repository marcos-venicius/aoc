package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		_, line := reader.Line()
		parsedLine := parseLine(line)

    if isSafe(parsedLine) {
      ans += 1
    }
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

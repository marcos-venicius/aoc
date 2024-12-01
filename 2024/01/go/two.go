package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	similarityScore := 0

	left := make(map[int]int)
	right := make(map[int]int)

	for reader.Running() {
		_, line := reader.Line()

		parsedLine := parseLine(line)

		left[parsedLine.left]++
		right[parsedLine.right]++
	}

	for k, v := range left {
		similarityScore += k * v * right[k]
	}

	fmt.Printf("02: %d\n", similarityScore)

	return similarityScore
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	input := CreateInput()

	for reader.Running() {
		_, line := reader.Line()

		input.ParseLine(line)
	}

	correct := input.getCorrectUpdatesIndexes()

	ans := input.sumIndexes(correct)

	fmt.Printf("01: %d\n", ans)

	return ans
}

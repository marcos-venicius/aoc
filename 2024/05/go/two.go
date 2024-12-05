package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	input := CreateInput()

	for reader.Running() {
		_, line := reader.Line()

		input.ParseLine(line)
	}

	incorrect := input.getIncorrectUpdatesIndexes()

	input.fixUpdates(incorrect)

	ans := input.sumIndexes(incorrect)

	fmt.Printf("02: %d\n", ans)

	return ans
}

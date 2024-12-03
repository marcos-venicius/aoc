package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0
	state := true

	for reader.Running() {
		_, line := reader.Line()

		expressions, finalState := parseCompleteExpressions(line, state)

		ans += evaluateExpressions(expressions)
		state = finalState
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
  input := CreateInput()

	for reader.Running() {
		_, line := reader.Line()

    input.parseLine(line)
	}

  ans := input.findChains()

	fmt.Printf("02: %d\n", ans)

	return ans
}

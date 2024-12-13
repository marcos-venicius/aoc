package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
  input := CreateInput()

	for reader.Running() {
		_, line := reader.Line()

    input.parseLine(line)
	}

  ans := input.findChains()

  heads := input.distinct()

	fmt.Printf("01: %d\n", heads)

	return ans
}

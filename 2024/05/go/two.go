package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		reader.Line()
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

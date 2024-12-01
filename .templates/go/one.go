package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	for reader.Running() {
		i, line := reader.Line()

		println(i, line)
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

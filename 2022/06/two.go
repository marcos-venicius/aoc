package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := solve(reader, 14)

	fmt.Printf("02: %d\n", ans)

	return ans
}

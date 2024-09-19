package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := solve(reader, 4)

	fmt.Printf("01: %d\n", ans)

	return ans
}

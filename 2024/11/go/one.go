package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	_, line := reader.Line()

  r := CreateResult(25)

	ans := r.GetResult(line)

	fmt.Printf("01: %d\n", ans)

	return ans
}

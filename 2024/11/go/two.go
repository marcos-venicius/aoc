package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader *aocreader.AocReader) int64 {
	_, line := reader.Line()

	r := CreateResult(line, 75)

	ans := r.GetResult()

	fmt.Printf("02: %d\n", ans)

	return ans
}

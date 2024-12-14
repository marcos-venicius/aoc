package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader *aocreader.AocReader) int64 {
	_, line := reader.Line()

	r := CreateResult(line, 25)

	ans := r.GetResult()

	fmt.Printf("01: %d\n", ans)

	return ans
}

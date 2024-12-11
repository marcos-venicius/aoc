package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int64 {
	_, line := reader.Line()

	blocks := parseIds(line)

	rearrangeFragmentedIds(blocks)

	ans := checksumIds(blocks)

	fmt.Printf("01: %d\n", ans)

	return ans
}

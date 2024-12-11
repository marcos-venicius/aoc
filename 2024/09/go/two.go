package main

import (
	"fmt"
	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int64 {
	_, line := reader.Line()

	blocks := parseIds(line)

	rearrangeIdBlocks(blocks)

	ans := checksumIds(blocks)

	fmt.Printf("02: %d\n", ans)

	return ans
}

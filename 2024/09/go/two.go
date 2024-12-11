package main

import (
	"fmt"
	"github.com/marcos-venicius/aocreader"
)

type Tuple struct {
	files     int
	freeSpace int
}

func solveTwo(reader aocreader.LinesReader) int64 {
	_, line := reader.Line()

	blocks := parseBlocks(line)

	rearrangeBlocks(blocks)

	ans := checksumFragmentedBlocks(blocks)

	fmt.Printf("02: %d\n", ans)
	return ans
}

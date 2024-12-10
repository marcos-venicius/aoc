package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int64 {
	_, line := reader.Line()

  blocks := parseBlocks(line, true)

	rearrangeFragmentedBlocks(blocks)

	ans := checksumFragmentedBlocks(blocks)

	fmt.Printf("01: %d\n", ans)

	return ans
}

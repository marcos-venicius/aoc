package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int64 {
	ans := int64(0)

	for reader.Running() {
		_, line := reader.Line()

    p := parseLine(line)

    if checkAnyCombinationMatchesTheNumberBase3(p) {
      ans += p.number
    }
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int64 {
	ans := int64(0)

	for reader.Running() {
		_, line := reader.Line()

		p := parseLine(line)

		combinations := getOperatorsCombinationsForLine(p)

		if checkAnyCombinationMatchesTheNumber(p, combinations) {
			ans += p.number
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

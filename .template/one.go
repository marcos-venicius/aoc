package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := 0

	reader.Read(func(line string) bool {
		return false
	})

	fmt.Printf("01: %d\n", ans)

	return ans
}

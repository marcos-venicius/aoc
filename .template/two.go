package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0

	reader.Read(func(line string) bool {
		return false
	})

	fmt.Printf("02: %d\n", ans)

	return 0
}

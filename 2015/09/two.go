package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	graph := CreateGraph()

  graph.SetComparator(MaxComparator)

	reader.Read(func(line string) bool {
		route := ParseLine(line)

		graph.Add(route)

		return false
	})

	ans := graph.Distance()

	fmt.Printf("02: %d\n", ans)

	return ans
}

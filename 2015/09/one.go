package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	graph := CreateGraph()

  graph.SetComparator(MinComparator)

	reader.Read(func(line string) bool {
		route := ParseLine(line)

		graph.Add(route)

		return false
	})

	ans := graph.Distance()

	fmt.Printf("01: %d\n", ans)

	return ans
}

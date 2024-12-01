package main

import (
	"fmt"
	"sort"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	distance := 0

	left := make([]int, 0)
	right := make([]int, 0)

	for reader.Running() {
		_, line := reader.Line()

		parsedLine := parseLine(line)

		left = append(left, parsedLine.left)
		right = append(right, parsedLine.right)
	}

	sort.Slice(left, func(i, j int) bool {
		return left[i] < left[j]
	})

	sort.Slice(right, func(i, j int) bool {
		return right[i] < right[j]
	})

	for i := 0; i < len(left); i++ {
		distance += abs(left[i] - right[i])
	}

	fmt.Printf("01: %d\n", distance)

	return distance
}

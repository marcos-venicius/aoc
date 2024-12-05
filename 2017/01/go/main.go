package main

import "github.com/marcos-venicius/aocreader"

func main() {
	reader := aocreader.NewAocReader("../input.txt")

	_, line := reader.Line()

	parsed := parseLine(line)

	solveOne(parsed)
	solveTwo(parsed)
}

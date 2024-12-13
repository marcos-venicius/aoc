package main

import "github.com/marcos-venicius/aocreader"

func main() {
	reader := aocreader.NewAocReader("../test.txt")

	solveOne(reader)

	reader.Reset()

	solveTwo(reader)
}

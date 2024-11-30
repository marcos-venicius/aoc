package main

import "github.com/marcos-venicius/aocreader"

func main() {
	reader := aocreader.NewAocReader("../input.txt")

	solveOne(reader)
	solveTwo(reader)
}

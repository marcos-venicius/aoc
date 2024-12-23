package main

import (
	"flag"

	"github.com/marcos-venicius/aocreader"
)

func main() {
	final := flag.Bool("final", false, "run final giant input")

	flag.Parse()

	var reader *aocreader.AocReader

	if *final {
		reader = aocreader.NewAocReader("../input.txt")
	} else {
		reader = aocreader.NewAocReader("../test.txt")
	}

	solveOne(reader)

	reader.Reset()

	solveTwo(reader)
}

// Attempts
// 1474029
// 1476258
// 1496444
// 1496472

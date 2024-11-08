package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	db := CreateDatabase()

	db.SetComparator(MaxComparator)

	reader.Read(func(line string) bool {
		route := ParseLine(line)

		db.Add(route)

		return false
	})

	ans, err := db.Distance()

	if err != nil {
		panic(err)
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	db := CreateDatabase()

	db.SetComparator(MinComparator)

	reader.Read(func(line string) bool {
		err := db.Add(line)

		if err != nil {
			panic(err)
		}

		return false
	})

	ans, err := db.Distance()

	if err != nil {
		panic(err)
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

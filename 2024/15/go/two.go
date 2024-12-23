package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) int {
	warehouse := CreateWarehouse()

	for reader.Running() {
		_, line := reader.Line()

		warehouse.ParseLine(line)
	}

	/* for _, movement := range warehouse.movements {
	} */

	warehouse.Display()

	ans := warehouse.SumBoxesCoordinates()

	fmt.Printf("02: %d\n", ans)

	return ans
}

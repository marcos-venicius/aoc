package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	warehouse := CreateWarehouse()

	for reader.Running() {
		_, line := reader.Line()

		warehouse.ParseLine(line)
	}

	for _, movement := range warehouse.movements {
		warehouse.Move(warehouse.robot, movement, true)
	}

	ans := warehouse.SumBoxesCoordinates()

	fmt.Printf("01: %d\n", ans)

	return ans
}

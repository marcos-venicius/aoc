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

  warehouse.GrowMap()

  println("Initial state:")
  warehouse.Display()
	for _, movement := range warehouse.movements {
    /* fmt.Printf("Move %c (%d, %d):\n", movement, warehouse.robot.x, warehouse.robot.y) */
		warehouse.MovePairs(warehouse.robot, movement, true)
    /* warehouse.Display() */
	}

  warehouse.Display()

	ans := warehouse.SumBoxesCoordinates()

	fmt.Printf("02: %d\n", ans)

	return ans
}

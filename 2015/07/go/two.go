package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveTwo(reader aocreader.LinesReader) uint16 {
	instructions := make([]Instruction, 0)

	reader.Read(func(line string) bool {
		instruction := ParseInstruction(line)

		instructions = append(instructions, instruction)

		return false
	})

	solve := NewSolve(instructions)

	ans := solve.Solve("a")

	bValue := solve.values["a"]
	solve.values = make(map[string]uint16)
	solve.values["b"] = bValue

	ans = solve.Solve("a")

	fmt.Printf("02: %d\n", ans)

	return ans
}

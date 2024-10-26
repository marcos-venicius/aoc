package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) uint16 {
	instructions := make([]Instruction, 0)

	reader.Read(func(line string) bool {
		instruction := ParseInstruction(line)

		instructions = append(instructions, instruction)

		return false
	})

	solve := NewSolve(instructions)

	ans := solve.Solve("a")

	fmt.Printf("01: %d\n", ans)

	return ans
}

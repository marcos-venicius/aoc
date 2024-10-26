package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/marcos-venicius/aocreader"
)

const (
	ASSIGN_VALUE_KIND = iota
	ASSIGN_VAR_KIND   = iota
	OR_KIND           = iota
	AND_KIND          = iota
	NOT_KIND          = iota
	LSHIFT_KIND       = iota
	RSHIFT_KIND       = iota
)

type Instruction struct {
	left   string
	right  string
	kind   int
	value  uint16
	output string
}

type Solve struct {
	values       map[string]uint16
	instructions map[string][]Instruction
}

func NewSolve(instructions []Instruction) *Solve {
	all := make(map[string][]Instruction)

	for _, instruction := range instructions {
		if _, ok := all[instruction.output]; !ok {
			all[instruction.output] = make([]Instruction, 0)
		}

		all[instruction.output] = append(all[instruction.output], instruction)
	}

	return &Solve{
		values:       make(map[string]uint16),
		instructions: all,
	}
}

func StringToType(str string) int {
	switch str {
	case "LSHIFT":
		return LSHIFT_KIND
	case "RSHIFT":
		return RSHIFT_KIND
	case "OR":
		return OR_KIND
	case "AND":
		return AND_KIND
	default:
		panic("invalid type")
	}
}

func ParseInstruction(line string) Instruction {
	instruction := Instruction{}

	split := strings.Split(line, " ")

	if len(split) == 3 {
		value, err := strconv.ParseInt(split[0], 10, 16)

		if err != nil {
			instruction.kind = ASSIGN_VAR_KIND
			instruction.left = split[0]
		} else {
			instruction.kind = ASSIGN_VALUE_KIND
			instruction.value = uint16(value)
		}
	} else if len(split) == 4 {
		instruction.kind = NOT_KIND
		instruction.left = split[1]
	} else if split[1] == "LSHIFT" || split[1] == "RSHIFT" {
		value, err := strconv.ParseInt(split[2], 10, 16)

		if err != nil {
			panic(err)
		}

		instruction.left = split[0]
		instruction.value = uint16(value)
		instruction.kind = StringToType(split[1])
	} else {
		instruction.left = split[0]
		instruction.right = split[2]
		instruction.kind = StringToType(split[1])
	}

	instruction.output = split[len(split)-1]

	return instruction
}

func (s *Solve) Evaluate(instruction Instruction) {
	switch instruction.kind {
	case ASSIGN_VALUE_KIND:
		s.values[instruction.output] = instruction.value
	case ASSIGN_VAR_KIND:
		if _, ok := s.values[instruction.left]; !ok {
			for _, missingInstruction := range s.instructions[instruction.left] {
				s.Evaluate(missingInstruction)
			}
		}

		s.values[instruction.output] = s.values[instruction.left]
	case LSHIFT_KIND, RSHIFT_KIND:
		if _, ok := s.values[instruction.left]; !ok {
			for _, missingInstruction := range s.instructions[instruction.left] {
				s.Evaluate(missingInstruction)
			}
		}

		leftValue := s.values[instruction.left]
		value := instruction.value

		switch instruction.kind {
		case LSHIFT_KIND:
			s.values[instruction.output] = leftValue << value
		case RSHIFT_KIND:
			s.values[instruction.output] = leftValue >> value
		}
	case NOT_KIND:
		if _, ok := s.values[instruction.left]; !ok {
			for _, missingInstruction := range s.instructions[instruction.left] {
				s.Evaluate(missingInstruction)
			}
		}

		varValue := s.values[instruction.left]

		s.values[instruction.output] = ^varValue
	default:
		var leftValue uint16
		var rightValue uint16

		if _, ok := s.values[instruction.left]; !ok {
			if _, ok := s.instructions[instruction.left]; ok {
				for _, missingInstrction := range s.instructions[instruction.left] {
					s.Evaluate(missingInstrction)
				}

				leftValue = s.values[instruction.left]
			} else {
				value, err := strconv.ParseInt(instruction.left, 10, 16)

				if err != nil {
					panic(err)
				}

				leftValue = uint16(value)
			}
		} else {
			leftValue = s.values[instruction.left]
		}

		if _, ok := s.values[instruction.right]; !ok {
			if _, ok := s.instructions[instruction.right]; ok {
				for _, missingInstrction := range s.instructions[instruction.right] {
					s.Evaluate(missingInstrction)
				}

				rightValue = s.values[instruction.right]
			} else {
				value, err := strconv.ParseInt(instruction.right, 10, 16)

				if err != nil {
					panic(err)
				}

				rightValue = uint16(value)
			}
		} else {
			rightValue = s.values[instruction.right]
		}

		switch instruction.kind {
		case AND_KIND:
			s.values[instruction.output] = leftValue & rightValue
		case OR_KIND:
			s.values[instruction.output] = leftValue | rightValue
		}
	}
}

func (s *Solve) Solve(variable string) uint16 {
	for _, instruction := range s.instructions[variable] {
		s.Evaluate(instruction)
	}

	return s.values[variable]
}

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

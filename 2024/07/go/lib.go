package main

import (
	"fmt"
	"math"
	"regexp"
	"strconv"
)

type Line struct {
	number  int64
	numbers []int
}

func parseLine(line string) Line {
	regex := regexp.MustCompile(`\d+`)

	found := regex.FindAllString(line, -1)

	pl := Line{}

	n, _ := strconv.ParseInt(found[0], 10, 64)

	pl.number = n

	for i := 1; i < len(found); i++ {
		n, _ := strconv.Atoi(found[i])

		pl.numbers = append(pl.numbers, n)
	}

	return pl
}

func base3(n int) []int {
  size := 64
	v := make([]int, 0, size)

	for n > 0 {
		v = append(v, n%3)
    n /= 3
	}

  v = append(v, n%3)

  for i := 0; i < size - len(v); i++ {
    v = append(v, 0)
  }

	return v
}

func isBitSet(n, pos int) bool {
	return (n & (1 << pos)) != 0
}

const (
	PLUS_OP   = iota
	TIMES_OP  = iota
	CONCAT_OP = iota
)

func getOperatorsCombinationsForLine(line Line) [][]int {
	differentCombinations := int(math.Pow(2, float64(len(line.numbers)-1)))

	operations := make([][]int, 0, differentCombinations)
	operatorsPlaces := len(line.numbers) - 1

	// Each number represent a different combination, which each bit from right to left
	// based on the amount of places possibles to have an operator.
	// "*" being 0
	// "+" being 1
	// so, we need to get the total amount of combinations possible and for each number we extract the bits
	// as the operatos
	for combination := 0; combination < differentCombinations; combination++ {
		operatorsCombination := make([]int, 0, operatorsPlaces)

		for operatorBitPosition := 0; operatorBitPosition < operatorsPlaces; operatorBitPosition++ {
			if isBitSet(combination, operatorBitPosition) {
				operatorsCombination = append(operatorsCombination, PLUS_OP)
			} else {
				operatorsCombination = append(operatorsCombination, TIMES_OP)
			}
		}

		operations = append(operations, operatorsCombination)
	}

	return operations
}

func checkAnyCombinationMatchesTheNumber(line Line, combinations [][]int) bool {
	for _, combination := range combinations {
		sum := int64(line.numbers[0])
		oi := 0

		for i := 1; i < len(line.numbers); i++ {
			operator := combination[oi]
			operand := line.numbers[i]

			if operator == PLUS_OP {
				sum += int64(operand)
			} else if operator == TIMES_OP {
				sum *= int64(operand)
			} else {
				panic("invalid operator")
			}

			oi++

			if sum > line.number {
				break
			}
		}

		if sum == line.number {
			return true
		}
	}

	return false
}

func checkAnyCombinationMatchesTheNumberBase3(line Line) bool {
	differentCombinations := int(math.Pow(3, float64(len(line.numbers)-1)))

	for combination := 0; combination < differentCombinations; combination++ {
		sum := int64(line.numbers[0])

		operators := base3(combination)

		for i := 1; i < len(line.numbers); i++ {
			operand := line.numbers[i]

			switch operators[i-1] {
			case 0:
				sum += int64(operand)
      case 1:
        sum *= int64(operand)
      case 2:
        n, _ := strconv.ParseInt(fmt.Sprintf("%d%d", sum, operand), 10, 64)
        
        sum = n
			}
		}

    if sum == line.number {
      return true
    }
	}

	return false
}

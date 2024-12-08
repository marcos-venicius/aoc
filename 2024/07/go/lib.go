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

func base3(n, size int) []int {
	v := make([]int, 0, size)

	for n > 0 {
		v = append(v, n%3)
		n /= 3
	}

	v = append(v, n%3)

	for i := 0; i < size-len(v); i++ {
		v = append(v, 0)
	}

	return v
}

func isBitSet(n, pos int) bool {
	return (n & (1 << pos)) != 0
}

func checkAnyCombinationMatchesTheNumber(line Line) bool {
	differentCombinations := int(math.Pow(3, float64(len(line.numbers)-1)))

	for combination := 0; combination < differentCombinations; combination++ {
		sum := int64(line.numbers[0])
		oi := 0

		for i := 1; i < len(line.numbers); i++ {
			operand := line.numbers[i]

			if isBitSet(combination, i-1) {
				sum += int64(operand)
			} else {
				sum *= int64(operand)
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

		operators := base3(combination, len(line.numbers)*2)

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

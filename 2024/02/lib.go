package main

import (
	"regexp"
	"strconv"
)

const (
	INC = iota
	DEC = iota
)

func parseLine(line string) []int {
	regex := regexp.MustCompile(`(\d+)`)

	result := regex.FindAllString(line, -1)

	numbers := make([]int, 0, len(result))

	for i := 0; i < len(result); i++ {
		number, err := strconv.Atoi(result[i])

		if err != nil {
			panic(err)
		}

		numbers = append(numbers, number)
	}

	return numbers
}

func inc(a, b int) bool {
	if b <= a {
		return false
	}

	if b-a < 1 || b-a > 3 {
		return false
	}

	return true
}

func dec(a, b int) bool {
	if b >= a {
		return false
	}

	if a-b < 1 || a-b > 3 {
		return false
	}

	return true
}

func isSafe(levels []int) bool {
	state := DEC

	if levels[1] > levels[0] {
		state = INC
	} else if levels[1] < levels[0] {
		state = DEC
	} else {
		return false
	}

	for i := 1; i < len(levels); i++ {
		switch state {
		case INC:
			if !inc(levels[i-1], levels[i]) {
				return false
			}
		case DEC:
			if !dec(levels[i-1], levels[i]) {
				return false
			}
		default:
			break
		}
	}

	return true
}

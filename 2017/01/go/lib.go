package main

func parseLine(line string) []int {
	digits := make([]int, len(line), len(line))

	for i, c := range line {
		digits[i] = int(c - '0')
	}

	return digits
}

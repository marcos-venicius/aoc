package main

func parseLine(line string) []int {
	digits := make([]int, len(line), len(line))

	for i, c := range line {
		digits[i] = int(c - '0')
	}

	return digits
}

func exploitCptcha(digits *[]int, by int) (s int) {
	for i, d := range *digits {
		next := (i + by) % len(*digits)

		if d == (*digits)[next] {
			s += d
		}
	}

	return
}

package main

import "strconv"

func prepare(line string) []int {
	i := 0
	split := make([]int, 0)

	for i < len(line) {
		s := 1
		c := line[i]

		i += 1

		for i < len(line) && line[i] == c {
			i += 1
			s += 1
		}

		v, _ := strconv.Atoi(string(c))

		split = append(split, s)
		split = append(split, v)

		if i >= len(line) {
			break
		}
	}

	return split
}

func solve(line string, until int) int {
	data := prepare(line)

	result := make([]int, 0)
	until = until - 1

	for x := 0; x < until; x++ {
		i := 0

		for i < len(data) {
			s := 1
			c := data[i]

			i += 1

			for i < len(data) && data[i] == c {
				i += 1
				s += 1
			}

			result = append(result, s)
			result = append(result, c)

			if i >= len(data) {
				break
			}
		}

		if x < until-1 {
			data = result
			result = make([]int, 0)
		}
	}

	return len(result)
}

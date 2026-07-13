package main

import (
	"fmt"
)

func isNiceTwo(line string) bool {
	firstRule, secondRule, m := false, false, make(map[string]int)

	for i := 1; i < len(line); i++ {
		// checks if the letter before and after i are the same
		if i < len(line)-1 && line[i-1] == line[i+1] {
			secondRule = true
		}

		// get a pair, for example "aa"
		p := string(line[i-1 : i+1])

		// check if this pair appeared before
		if v, ok := m[p]; ok {
			// check if the first index of the current pair
			// is greater than the last index of the last same pair
			if i-1 > v {
				firstRule = true
			}
		} else {
			// saves the last index of the current pair
			// if not created yet
			m[p] = i
			// we need to save only the first appearance of a pair because
			// if we have something like "aaaa" and I save everytime, when
			// we verify "..aa", the last pair will be 1 2 (".aa."), so
			// the last index will equal to the current one
		}
	}

	return firstRule && secondRule
}

func solveTwo(lines []string) int {
	ans := 0

	for _, line := range lines {
		if isNiceTwo(line) {
			ans++
		}
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

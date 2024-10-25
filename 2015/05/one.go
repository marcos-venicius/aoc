package main

import (
	"fmt"
)

func isNice(line string) bool {
	vc, sc, ic := 0, 0, 0

	for i, c := range line {
		if isVowel(c) {
			vc++
		}

		if i > 0 && line[i] == line[i-1] {
			sc++
		}

		if i > 0 && isIlegal(rune(line[i-1]), rune(line[i])) {
			ic++
		}
	}

	return vc >= 3 && sc >= 1 && ic == 0
}

func solveOne(lines []string) int {
	ans := 0

	for _, line := range lines {
		if isNice(line) {
			ans++
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

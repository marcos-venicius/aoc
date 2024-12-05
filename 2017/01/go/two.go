package main

import (
	"fmt"
)

func solveTwo(digits []int) int {
	ans := exploitCptcha(&digits, len(digits)/2)

	fmt.Printf("02: %d\n", ans)

	return ans
}

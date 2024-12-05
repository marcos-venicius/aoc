package main

import (
	"fmt"
)

func solveOne(digits []int) int {
	ans := exploitCptcha(&digits, 1)

	fmt.Printf("01: %d\n", ans)

	return ans
}

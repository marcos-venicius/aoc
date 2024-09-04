package main

import (
	"fmt"
)

func solveTwo(lines []string) {
  i, r := 0, 0

  for ;; i++ {
    h := hash(lines[0], i)

    if startsWith6(h) {
      r = i
      break
    }
  }


  fmt.Printf("02: %d\n", r)
}

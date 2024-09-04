package main

import (
	"fmt"
  "crypto/md5"
)

func hash(input string, n int) [16]byte {
  data := []byte(fmt.Sprintf("%s%d", input, n))
  return md5.Sum(data)
}

func solveOne(lines []string) {
  i, r := 0, 0

  for ;; i++ {
    h := hash(lines[0], i)

    if startsWith5(h) {
      r = i
      break
    }
  }


  fmt.Printf("01: %d\n", r)
}

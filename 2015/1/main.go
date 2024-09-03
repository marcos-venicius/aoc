package main

import (
  "fmt"
  "io"
  "os"
  "log"
  "bufio"
)

type handler func(int) bool

func iterator(h handler) {
  t := map[byte]int{
    '(': 1,
    ')': -1,
  }

  f, err := os.Open("./input.txt")

  if err != nil {
    log.Fatal(err)
  }

  bs := 1024

  r := bufio.NewReader(f)
  
  buf := make([]byte, bs, bs)

  for {
    n, err := r.Read(buf)

    if (err != nil && err == io.EOF) || n == 0 {
      break
    }

    for _, b := range buf[:n] {
      if h(t[b]) {
        return
      }
    }

    if n < bs {
      break
    }
  }
}

func solve1() int {
  ans := 0

  iterator(func(n int) bool {
    ans += n

    return false
  })

  return ans
}

func solve2() int {
  ans, index := 0, 0

  iterator(func(n int) bool {
    index++
    ans += n

    if ans == -1 {
      return true
    }

    return false
  })

  return index
}

func main() {
  fmt.Println(solve1())
  fmt.Println(solve2())
}

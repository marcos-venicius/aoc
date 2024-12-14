package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/marcos-venicius/aocreader"
)

func trimZeros(v string) string {
  if v[0] != '0' {
    return v
  }

  for i := 0; i < len(v); i++ {
    if v[i] != '0' {
      return v[i:]
    } else if v[i] == '0' && i == len(v) - 1 {
      return "0"
    }
  }

  return v
}

func applyRules(to []string, iteration int) []string {
	if iteration == 25 {
		return to
	}

	out := make([]string, 0)

  for _, v := range to {

		if v == "0" {
      out = append(out, "1")
		} else if len(v)%2 == 0 {
			m := len(v) / 2

			out = append(out, trimZeros(v[:m]))
			out = append(out, trimZeros(v[m:]))
		} else {
			vi, _ := strconv.ParseInt(v, 10, 63)
      res := vi*2024

			out = append(out, strconv.FormatInt(res, 10))
		}
	}

	return applyRules(out, iteration+1)
}

func solveOne(reader aocreader.LinesReader) int {
	_, line := reader.Line()

  out := applyRules(strings.Split(line, " "), 0)

	ans := len(out)

	fmt.Printf("01: %d\n", ans)

	return ans
}

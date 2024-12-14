package main

import (
	"strconv"
	"strings"
)

type Result struct {
  iterations int
}

func CreateResult(iterations int) Result {
  return Result{
    iterations: iterations,
  }
}

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

func (r *Result) applyRules(to []string, iteration int) []string {
	if iteration == r.iterations {
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

	return r.applyRules(out, iteration+1)
}

func (r *Result) GetResult(line string) int {
  out := r.applyRules(strings.Split(line, " "), 0)

  return len(out)
}

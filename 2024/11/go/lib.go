package main

import (
	"strconv"
	"strings"
)

type Key struct {
	number int64
	steps  int
}

type Result struct {
	iterations int
	cache      map[Key]int64
	numbers    []string
}

func CreateResult(line string, iterations int) Result {
	return Result{
		iterations: iterations,
		cache:      make(map[Key]int64),
		numbers:    strings.Split(line, " "),
	}
}

func trimZeros(v string) string {
	if v[0] != '0' {
		return v
	}

	for i := 0; i < len(v); i++ {
		if v[i] != '0' {
			return v[i:]
		} else if v[i] == '0' && i == len(v)-1 {
			return "0"
		}
	}

	return v
}

func unwrap[T int64](v T, err error) T {
	if err != nil {
		panic(err)
	}

	return v
}

func (rs *Result) calcLength(number int64, steps int) int64 {
	if steps == 0 {
		return 1
	}

	key := Key{number: number, steps: steps}

	if _, ok := rs.cache[key]; !ok {
		var result int64 = 0

		if number == 0 {
			result = rs.calcLength(1, steps-1)
		} else if len(strconv.FormatInt(number, 10))%2 == 0 {
			s := strconv.FormatInt(number, 10)
			m := len(s) / 2

			l := unwrap(strconv.ParseInt(s[:m], 10, 64))
			r := unwrap(strconv.ParseInt(s[m:], 10, 64))

			result += rs.calcLength(l, steps-1)
			result += rs.calcLength(r, steps-1)
		} else {
			result = rs.calcLength(number*2024, steps-1)
		}

		rs.cache[key] = result
	}

	return rs.cache[key]
}

func (r *Result) GetResult() int64 {
	var s int64 = 0

	for _, n := range r.numbers {
		s += r.calcLength(unwrap(strconv.ParseInt(n, 10, 64)), r.iterations)
	}

	return s
}

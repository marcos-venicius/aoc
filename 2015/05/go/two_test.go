package main

import "testing"

func TestSolveTwo(t *testing.T) {
	data := map[string]int{
		"qjhvhtzxzqqjkmpb": 1,
		"xxyxx":            1,
		"uurcxstgmygtbstg": 0,
		"ieodomkazucvgmuy": 0,
		"aaaa":             1,
		"aaa":              0,
		"aaabcb":           0,
	}

	for k, v := range data {
		r := solveTwo([]string{k})

		if r != v {
			t.Fatalf("%d not equal to %d", r, v)
		}
	}
}

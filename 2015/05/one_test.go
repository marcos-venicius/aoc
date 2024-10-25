package main

import "testing"

func TestSolveOne(t *testing.T) {
	data := map[string]int{
		"aaa":              1,
		"ugknbfddgicrmopn": 1,
		"jchzalrnumimnmhp": 0,
		"haegwjzuvuyypxyu": 0,
		"dvszwmarrgswjxmb": 0,
	}

	for k, v := range data {
		r := solveOne([]string{k})

		if r != v {
			t.Fatalf("%d not equal to %d", r, v)
		}
	}
}

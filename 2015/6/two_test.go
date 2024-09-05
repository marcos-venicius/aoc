package main

import "testing"

func TestTurnOnOne(t *testing.T) {
	lines := []string{
		"turn on 0,0 through 0,0",
	}

	r := solveTwo(lines)
	expected := 1

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

func TestToggleAll(t *testing.T) {
	lines := []string{
		"toggle 0,0 through 999,999",
	}

	r := solveTwo(lines)
	expected := 2_000_000

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

func TestFullInputTwo(t *testing.T) {
	lines := readLines()

	r := solveTwo(lines)
	expected := 15_343_601

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

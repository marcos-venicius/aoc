package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
)

func TestTurnOnOne(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
		"turn on 0,0 through 0,0",
	})

	r := solveTwo(reader)
	expected := 1

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

func TestToggleAll(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
		"toggle 0,0 through 999,999",
	})

	r := solveTwo(reader)
	expected := 2_000_000

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

func TestFullInputTwo(t *testing.T) {
	reader := aocreader.NewAocReader("./input.txt")

	r := solveTwo(reader)
	expected := 15_343_601

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

package main

import (
	"testing"
)

func TestTurningOnEverythingOn(t *testing.T) {
	reader := NewFakeReader([]string{
		"turn on 0,0 through 999,999",
	})

	result := solveOne(reader)
	expected := 1_000_000

	if result != expected {
		t.Fatalf("%d != %d", result, expected)
	}
}

func TestTurningOffEverythingOn(t *testing.T) {
	reader := NewFakeReader([]string{
		"turn off 0,0 through 999,999",
	})

	result := solveOne(reader)
	expected := 0

	if result != expected {
		t.Fatalf("%d != %d", result, expected)
	}
}

func TestTogglingEverythingOn(t *testing.T) {
	reader := NewFakeReader([]string{
		"toggle 0,0 through 999,999",
	})

	result := solveOne(reader)
	expected := 1_000_000

	if result != expected {
		t.Fatalf("%d != %d", result, expected)
	}
}

func TestTurningAChunkOn(t *testing.T) {
	reader := NewFakeReader([]string{
		"toggle 50,50 through 60,60",   // 11x11 = 121
		"turn on 10,10 through 20,20",  // 11x11 = 121
		"turn off 15,15 through 20,20", // 6x6   = 36
	})

	result := solveOne(reader)
	expected := 206

	if result != expected {
		t.Fatalf("%d != %d", result, expected)
	}
}

func TestFullInputOne(t *testing.T) {
	reader := NewReader("./input.txt")

	r := solveOne(reader)
	expected := 400_410

	if r != expected {
		t.Fatalf("%d != %d", r, expected)
	}
}

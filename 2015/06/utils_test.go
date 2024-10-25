package main

import "testing"

func TestParseLineTurningOn(t *testing.T) {
	line := parseLine("turn on 0,0 through 999,999")

	if line.action != turnLightOn {
		t.Fatalf("%d != %d", line.action, turnLightOn)
	}

	if line.from.x != 0 {
		t.Fatalf("%d != %d", line.from.x, 0)
	}

	if line.from.y != 0 {
		t.Fatalf("%d != %d", line.from.y, 0)
	}

	if line.to.x != 999 {
		t.Fatalf("%d != %d", line.to.x, 999)
	}

	if line.to.y != 999 {
		t.Fatalf("%d != %d", line.to.y, 999)
	}
}

func TestParseLineTurningOf(t *testing.T) {
	line := parseLine("turn off 499,499 through 500,500")

	if line.action != turnLightOff {
		t.Fatalf("%d != %d", line.action, turnLightOff)
	}

	if line.from.x != 499 {
		t.Fatalf("%d != %d", line.from.x, 499)
	}

	if line.from.y != 499 {
		t.Fatalf("%d != %d", line.from.y, 499)
	}

	if line.to.x != 500 {
		t.Fatalf("%d != %d", line.to.x, 500)
	}

	if line.to.y != 500 {
		t.Fatalf("%d != %d", line.to.y, 500)
	}
}

func TestParseLineToggling(t *testing.T) {
	line := parseLine("toggle 0,0 through 999,0")

	if line.action != toggleLight {
		t.Fatalf("%d != %d", line.action, toggleLight)
	}

	if line.from.x != 0 {
		t.Fatalf("%d != %d", line.from.x, 0)
	}

	if line.from.y != 0 {
		t.Fatalf("%d != %d", line.from.y, 0)
	}

	if line.to.x != 999 {
		t.Fatalf("%d != %d", line.to.x, 999)
	}

	if line.to.y != 0 {
		t.Fatalf("%d != %d", line.to.y, 0)
	}
}

package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewMockReader([]string{})

	solveTwo(reader)

	t.Fail()
}

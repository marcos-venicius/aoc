package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewMockReader([]string{})

	solveOne(reader)

	t.Fail()
}

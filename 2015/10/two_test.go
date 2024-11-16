package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewAocReader("input.txt")

	r := solveTwo(reader)

	assert.Equal(t, 6989950, r)
}

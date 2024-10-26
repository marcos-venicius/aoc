package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewAocReader("./input.txt")

	res := solveTwo(reader)

	assert.Equal(t, uint16(2797), res)
}

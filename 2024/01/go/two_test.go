package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
		"3   4",
		"4   3",
		"2   5",
		"1   3",
		"3   9",
		"3   3",
	})

	res := solveTwo(reader)

	assert.Equal(t, 31, res)
}

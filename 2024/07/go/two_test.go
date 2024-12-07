package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewMockReader([]string{})

	solveTwo(reader)

	assert.Equal(t, 0, 1)
}

package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewMockReader([]string{})

	solveOne(reader)

	assert.Equal(t, 0, 1)
}

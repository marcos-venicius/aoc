package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	assert.Equal(t, solveOne(aocreader.NewMockReader([]string{"1122"})), 3)
	assert.Equal(t, solveOne(aocreader.NewMockReader([]string{"1111"})), 4)
	assert.Equal(t, solveOne(aocreader.NewMockReader([]string{"1234"})), 0)
	assert.Equal(t, solveOne(aocreader.NewMockReader([]string{"91212129"})), 9)
}

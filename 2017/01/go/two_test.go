package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	assert.Equal(t, solveTwo([]int{1, 2, 1, 2}), 6)
	assert.Equal(t, solveTwo([]int{1, 2, 2, 1}), 0)
	assert.Equal(t, solveTwo([]int{1, 2, 3, 4, 2, 5}), 4)
	assert.Equal(t, solveTwo([]int{1, 2, 3, 1, 2, 3}), 12)
	assert.Equal(t, solveTwo([]int{1, 2, 1, 3, 1, 4, 1, 5}), 4)
}

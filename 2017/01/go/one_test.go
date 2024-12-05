package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	assert.Equal(t, solveOne([]int{1, 1, 2, 2}), 3)
	assert.Equal(t, solveOne([]int{1, 1, 1, 1}), 4)
	assert.Equal(t, solveOne([]int{1, 2, 3, 4}), 0)
	assert.Equal(t, solveOne([]int{9, 1, 2, 1, 2, 1, 2, 9}), 9)
}

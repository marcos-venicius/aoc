package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	input := Input{}

	solveOne(input)

	assert.Equal(t, 0, 1)
}

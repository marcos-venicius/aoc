package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewAocReader("input.txt")

	r := solveOne(reader)

	assert.Equal(t, 492982, r)
}

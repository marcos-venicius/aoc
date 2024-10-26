package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewAocReader("./input.txt")

  res := solveOne(reader)

  assert.Equal(t, uint16(16076), res)
}

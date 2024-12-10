package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
    "2333133121414131402",
  })

  ans := solveTwo(reader)

	assert.Equal(t, int64(2858), ans)
}

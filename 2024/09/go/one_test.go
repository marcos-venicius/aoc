package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
    "2333133121414131402",
  })

  ans := solveOne(reader)

	assert.Equal(t, int64(1928), ans)
}

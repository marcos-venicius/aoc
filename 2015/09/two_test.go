package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
    "London to Dublin = 464",
    "London to Belfast = 518",
    "Dublin to Belfast = 141",
  })

  ans := solveTwo(reader)

  assert.Equal(t, 982, ans)
}

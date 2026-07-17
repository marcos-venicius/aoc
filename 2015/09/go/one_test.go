package main

import (
	"testing"

	"github.com/marcos-venicius/aocreader"
	"github.com/stretchr/testify/assert"
)

func TestBaseOne(t *testing.T) {
	reader := aocreader.NewMockReader([]string{
		"London to Dublin = 464",
		"London to Belfast = 518",
		"Dublin to Belfast = 141",
	})

	ans := solveOne(reader)

	assert.Equal(t, 605, ans)
}

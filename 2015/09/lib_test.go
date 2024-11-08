package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGraph(t *testing.T) {
	db := CreateDatabase()

	lines := []string{
		"London to Dublin = 464",
		"London to Belfast = 518",
		"Dublin to Belfast = 141",
	}

	for _, line := range lines {
		route := ParseLine(line)

		db.Add(route)
	}

	assert.Equal(t, 3, len(db.routes))
	assert.Equal(t, 3, len(db.locations))

	assert.Equal(t, 464, db.routes["London"]["Dublin"])
	assert.Equal(t, 464, db.routes["Dublin"]["London"])

	assert.Equal(t, 518, db.routes["London"]["Belfast"])
	assert.Equal(t, 518, db.routes["Belfast"]["London"])

	assert.Equal(t, 141, db.routes["Dublin"]["Belfast"])
	assert.Equal(t, 141, db.routes["Belfast"]["Dublin"])
}

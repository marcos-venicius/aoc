package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDatabase(t *testing.T) {
	db := CreateDatabase()

	lines := []string{
		"London to Dublin = 464",
		"London to Belfast = 518",
		"Dublin to Belfast = 141",
	}

	for _, line := range lines {
		err := db.Add(line)

		assert.Nil(t, err)
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

func TestRouteParser(t *testing.T) {
	db := CreateDatabase()

	r1 := "London to       Dublin = 464"
	r2 := "London to Belfast=518"
	r3 := "Dublin to Belfast          =      141"

	rs1, err := db.parseRoute(r1)

	assert.Nil(t, err)

	rs2, err := db.parseRoute(r2)

	assert.Nil(t, err)

	rs3, err := db.parseRoute(r3)

	assert.Nil(t, err)

	assert.Equal(t, "London", rs1.origin)
	assert.Equal(t, "Dublin", rs1.destination)
	assert.Equal(t, 464, rs1.distance)

	assert.Equal(t, "London", rs2.origin)
	assert.Equal(t, "Belfast", rs2.destination)
	assert.Equal(t, 518, rs2.distance)

	assert.Equal(t, "Dublin", rs3.origin)
	assert.Equal(t, "Belfast", rs3.destination)
	assert.Equal(t, 141, rs3.distance)
}

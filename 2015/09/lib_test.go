package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGraph(t *testing.T) {
  graph := CreateGraph()

  lines := []string{
    "London to Dublin = 464",
    "London to Belfast = 518",
    "Dublin to Belfast = 141",
  }

  for _, line := range lines {
    route := ParseLine(line)

    graph.Add(route)
  }

  assert.Equal(t, 3, len(graph.graph))
  assert.Equal(t, 3, len(graph.uniqueRoutes))

  assert.Equal(t, 464, graph.graph["London"]["Dublin"])
  assert.Equal(t, 464, graph.graph["Dublin"]["London"])

  assert.Equal(t, 518, graph.graph["London"]["Belfast"])
  assert.Equal(t, 518, graph.graph["Belfast"]["London"])

  assert.Equal(t, 141, graph.graph["Dublin"]["Belfast"])
  assert.Equal(t, 141, graph.graph["Belfast"]["Dublin"])
}


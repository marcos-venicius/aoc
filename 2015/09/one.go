package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/marcos-venicius/aocreader"
)

type Graph struct {
	graph        map[string]map[string]int
	uniqueRoutes map[string]struct{}
}

type Path struct {
	origin      string
	destination string
}

type Route struct {
	path Path

	distance int
}

func ParseLine(line string) Route {
	split := strings.Split(line, " ")

	from := split[0]
	to := split[2]
	distance := split[len(split)-1]

	distanceAsInteger, err := strconv.ParseInt(distance, 10, 32)

	if err != nil {
		panic(err)
	}

	return Route{
		path: Path{
			origin:      from,
			destination: to,
		},
		distance: int(distanceAsInteger),
	}
}

func CreateGraph() *Graph {
	return &Graph{
		graph:        make(map[string]map[string]int),
		uniqueRoutes: make(map[string]struct{}),
	}
}

func (g *Graph) Add(route Route) {
	if _, ok := g.graph[route.path.origin]; !ok {
		g.graph[route.path.origin] = make(map[string]int)
	}

	if _, ok := g.graph[route.path.destination]; !ok {
		g.graph[route.path.destination] = make(map[string]int)
	}

	g.graph[route.path.origin][route.path.destination] = route.distance
	g.graph[route.path.destination][route.path.origin] = route.distance

	g.uniqueRoutes[route.path.origin] = struct{}{}
	g.uniqueRoutes[route.path.destination] = struct{}{}
}

func (g *Graph) MinNextDistance(origin string, distance int, visited map[string]struct{}) int {
  if _, ok := visited[origin]; ok {
    return distance
  }

  visited[origin] = struct{}{}

  k, m := "", -1

  for key, distance := range g.graph[origin] {
    if _, ok := visited[key]; !ok && (m == -1 || distance < m) {
      m = distance
      k = key
    }
  }

  if m == -1 {
    return distance
  }

  return g.MinNextDistance(k, distance + m, visited)
}

func (g *Graph) ShortestDistance() int {
  distances := make([]int, 0)

	for route := range g.uniqueRoutes {
    amount := g.MinNextDistance(route, 0, make(map[string]struct{}))

    distances = append(distances, amount)
	}

  m := distances[0]

  for _, v := range distances {
    if v < m {
      m = v
    }
  }

  return m
}

func solveOne(reader aocreader.LinesReader) int {
	graph := CreateGraph()

	reader.Read(func(line string) bool {
		route := ParseLine(line)

		graph.Add(route)

		return false
	})

	ans := graph.ShortestDistance()

	fmt.Printf("01: %d\n", ans)

	return ans
}

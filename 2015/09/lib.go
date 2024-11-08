package main

import (
	"strconv"
	"strings"
)

type Comparator func(a, b int) bool

type Graph struct {
	graph        map[string]map[string]int
	uniqueRoutes map[string]struct{}
  comparator Comparator
}

type Path struct {
	origin      string
	destination string
}

type Route struct {
	path Path

	distance int
}

func MinComparator(a, b int) bool {
  return a < b
}

func MaxComparator(a, b int) bool {
  return a > b
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

func (g *Graph) SetComparator(comparator Comparator) {
  g.comparator = comparator
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

func (g *Graph) NextDistance(origin string, distance int, visited map[string]struct{}) int {
  if _, ok := visited[origin]; ok {
    return distance
  }

  visited[origin] = struct{}{}

  k, m := "", -1

  for key, distance := range g.graph[origin] {
    if _, ok := visited[key]; !ok && (m == -1 || g.comparator(distance, m)) {
      m = distance
      k = key
    }
  }

  if m == -1 {
    return distance
  }

  return g.NextDistance(k, distance + m, visited)
}

func (g *Graph) Distance() int {
  distances := make([]int, 0)

	for route := range g.uniqueRoutes {
    amount := g.NextDistance(route, 0, make(map[string]struct{}))

    distances = append(distances, amount)
	}

  m := distances[0]

  for _, v := range distances {
    if g.comparator(v, m) {
      m = v
    }
  }

  return m
}


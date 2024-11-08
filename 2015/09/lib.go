package main

import (
	"errors"
	"strconv"
	"strings"
)

type Comparator func(a, b int) bool

type Database struct {
	// store [origin][destination]distance
	routes     map[string]map[string]int
	locations  map[string]struct{}
	comparator Comparator
}

type Route struct {
	origin      string
	destination string
	distance    int
}

func MinComparator(a, b int) bool {
	return a < b
}

func MaxComparator(a, b int) bool {
	return a > b
}

func ParseLine(line string) Route {
	split := strings.Split(line, " ")

	origin := split[0]
	destination := split[2]
	distance := split[len(split)-1]

	distanceAsInteger, err := strconv.ParseInt(distance, 10, 32)

	if err != nil {
		panic(err)
	}

	return Route{
		origin:      origin,
		destination: destination,
		distance:    int(distanceAsInteger),
	}
}

func CreateDatabase() *Database {
	return &Database{
		routes:    make(map[string]map[string]int),
		locations: make(map[string]struct{}),
	}
}

func (d *Database) SetComparator(comparator Comparator) {
	d.comparator = comparator
}

func (d *Database) Add(route Route) {
	if _, ok := d.routes[route.origin]; !ok {
		d.routes[route.origin] = make(map[string]int)
	}

	if _, ok := d.routes[route.destination]; !ok {
		d.routes[route.destination] = make(map[string]int)
	}

	// saves 2-way directions, round trip.
	d.routes[route.origin][route.destination] = route.distance
	d.routes[route.destination][route.origin] = route.distance

	d.locations[route.origin] = struct{}{}
	d.locations[route.destination] = struct{}{}
}

func (d *Database) nextDistance(origin string, distance int, visited map[string]struct{}) int {
	visited[origin] = struct{}{}

	route, routeDistance := "", -1

	for key, distance := range d.routes[origin] {
		if _, ok := visited[key]; ok {
			continue
		}

		if routeDistance == -1 || d.comparator(distance, routeDistance) {
			routeDistance = distance
			route = key
		}
	}

	if routeDistance == -1 {
		return distance
	}

	return d.nextDistance(route, distance+routeDistance, visited)
}

func (d *Database) Distance() (int, error) {
	if d.comparator == nil {
		return 0, errors.New("no comparator was configured, please set a comparator before calling this function")
	}

	distances := make([]int, 0)

	for route := range d.locations {
		amount := d.nextDistance(route, 0, make(map[string]struct{}))

		distances = append(distances, amount)
	}

	m := distances[0]

	for _, v := range distances[1:] {
		if d.comparator(v, m) {
			m = v
		}
	}

	return m, nil
}

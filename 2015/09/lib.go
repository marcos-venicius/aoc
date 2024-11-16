package main

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
)

type Comparator func(a, b int) bool

type Database struct {
	// store [origin][destination]distance
	routes       map[string]map[string]int
	locations    map[string]struct{}
	comparator   Comparator
	routePattern *regexp.Regexp
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

func (d *Database) parseRoute(line string) (*Route, error) {
	matches := d.routePattern.FindStringSubmatch(line)

	if len(matches) < 7 {
		return nil, errors.New(fmt.Sprintf(`"%s" isn't a valid route`, line))
	}

	origin, destination, distance := matches[2], matches[3], matches[6]

	distanceAsInteger, err := strconv.ParseInt(distance, 10, 32)

	if err != nil {
		return nil, err
	}

	return &Route{
		origin:      origin,
		destination: destination,
		distance:    int(distanceAsInteger),
	}, nil
}

func CreateDatabase() *Database {
	routePattern := regexp.MustCompile(`^(\s?)*([A-z]+)\s+to\s+([A-z]+)(\s?)*=(\s?)*([0-9]+)$`)

	return &Database{
		routes:       make(map[string]map[string]int),
		locations:    make(map[string]struct{}),
		comparator:   nil,
		routePattern: routePattern,
	}
}

func (d *Database) SetComparator(comparator Comparator) {
	d.comparator = comparator
}

// Add Trys to add a new string line as a route, the format is "<From> to <Destination> = <distance>"
func (d *Database) Add(line string) error {
	route, err := d.parseRoute(line)

	if err != nil {
		return err
	}

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

	return nil
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

	distance := -1

	for route := range d.locations {
		amount := d.nextDistance(route, 0, make(map[string]struct{}))

		if distance == -1 || d.comparator(amount, distance) {
			distance = amount
		}
	}

	return distance, nil
}

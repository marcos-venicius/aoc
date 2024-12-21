package main

import (
	"regexp"
	"strconv"
)

type Vec2 struct {
	x, y int
}

type Robot struct {
	id  int
	pos Vec2
	vel Vec2
}

func unwrap[T any](data T, err error) T {
	if err != nil {
		panic(err)
	}

	return data
}

func mod(a, b int) int {
	return (a%b + b) % b
}

func (r *Robot) move(w, h int) {
	r.pos.x = mod(r.pos.x+r.vel.x, w)
	r.pos.y = mod(r.pos.y+r.vel.y, h)
}

func unique(list []int) int {
	m := make(map[int]struct{})

	for _, i := range list {
		m[i] = struct{}{}
	}

	return len(m)
}

func getQuadrant(x, y, w, h int) Vec2 {
	mw := w / 2
	mh := h / 2

	rx, ry := 0, 0

	if x > mw {
		rx = 1
	}

	if y > mh {
		ry = 1
	}

	return Vec2{x: rx, y: ry}
}

func parseRobot(id int, line string) Robot {
	regex := regexp.MustCompile(`(-?\d+)`)

	matches := regex.FindAllString(line, -1)

	x, y := unwrap(strconv.Atoi(matches[0])), unwrap(strconv.Atoi(matches[1]))
	vx, vy := unwrap(strconv.Atoi(matches[2])), unwrap(strconv.Atoi(matches[3]))

	return Robot{
		id: id,
		pos: Vec2{
			x: x,
			y: y,
		},
		vel: Vec2{
			x: vx,
			y: vy,
		},
	}
}

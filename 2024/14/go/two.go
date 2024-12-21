package main

import (
	"fmt"

	"github.com/marcos-venicius/aocreader"
)

func searchShape(robotsPosition map[Vec2]struct{}, x, y, w, h int) bool {
	center := Vec2{x: x, y: y}

	shape := [][]Vec2{
		{{0, 0}, {1, 0}, {2, 0}},
		{{0, 1}, {1, 1}, {2, 1}},
		{{0, 2}, {1, 2}, {2, 2}},
	}

	for _, row := range shape {
		for _, v := range row {
			center.x = x + v.x
			center.y = y + v.y

			if center.x <= 0 || center.y <= 0 || center.x >= w-1 || center.y >= h-1 {
				return false
			}

			if _, ok := robotsPosition[center]; !ok {
				return false
			}
		}
	}

	return true
}

func solveTwo(reader aocreader.LinesReader) int {
	ans := 0

	robots := make([]*Robot, 0)

	h, w := 0, 0

	for reader.Running() {
		index, line := reader.Line()

		robot := parseRobot(index+1, line)

		h = max(robot.pos.y+1, h)
		w = max(robot.pos.x+1, w)

		robots = append(robots, &robot)
	}

outer:
	for {
		ans++

		robotsPosition := make(map[Vec2]struct{})

		for _, robot := range robots {
			robot.move(w, h)

			robotsPosition[robot.pos] = struct{}{}
		}

		for robot := range robotsPosition {
			if searchShape(robotsPosition, robot.x, robot.y, w, h) {
				break outer
			}
		}
	}

	fmt.Printf("02: %d\n", ans)

	return ans
}

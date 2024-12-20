package main

import (
	"fmt"
	"sync"

	"github.com/marcos-venicius/aocreader"
)

func solveOne(reader aocreader.LinesReader) int {
	ans := -1

	robots := make([]*Robot, 0)
	robotsPerPos := make(map[Vec2][]int)

	h, w := 0, 0

	for reader.Running() {
		index, line := reader.Line()

		robot := parseRobot(index+1, line)

		h = max(robot.pos.y+1, h)
		w = max(robot.pos.x+1, w)

		robots = append(robots, &robot)
	}

	var wg sync.WaitGroup

	for _, robot := range robots {
		wg.Add(1)

		go func() {
			defer wg.Done()

			for i := 0; i < 100; i++ {
				robot.move(w, h)
			}
		}()
	}

	wg.Wait()

	for _, robot := range robots {
		if _, ok := robotsPerPos[robot.pos]; !ok {
			robotsPerPos[robot.pos] = make([]int, 0)
		}

		robotsPerPos[robot.pos] = append(robotsPerPos[robot.pos], robot.id)
	}

	quadrants := make(map[Vec2]int)

	for y := 0; y < h; y++ {
		if y == h/2 {
			continue
		}

		for x := 0; x < w; x++ {
			if x == w/2 {
				continue
			}

			if c, ok := robotsPerPos[Vec2{x: x, y: y}]; ok {
				quadrant := getQuadrant(x, y, w, h)

				quadrants[quadrant] += unique(c)
			}
		}
	}

	for _, v := range quadrants {
		if ans == -1 {
			ans = v
		} else {
			ans *= v
		}
	}

	fmt.Printf("01: %d\n", ans)

	return ans
}

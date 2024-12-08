package main

import "github.com/marcos-venicius/aocreader"

type Vector2 struct{ x, y int }

func parseInput(reader aocreader.LinesReader) [][]rune {
	data := make([][]rune, 0)

	for reader.Running() {
		_, line := reader.Line()

		data = append(data, []rune(line))
	}

	return data
}

func isOutOfBounds(x, y, w, h int) bool {
	return !(x >= 0 && x < w && y >= 0 && y < h)
}

package main

import "github.com/marcos-venicius/aocreader"

type Vector2 struct{ x, y int }

func parseInput(reader aocreader.LinesReader) []string {
	data := make([]string, 0)

	for reader.Running() {
		_, line := reader.Line()

		data = append(data, line)
	}

	return data
}

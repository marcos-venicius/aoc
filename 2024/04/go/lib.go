package main

import (
	"fmt"
	"os"
	"strings"
)

type Input struct {
	width, height int
	data          [][]byte
}

func readFile(path string) []byte {
	data, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	return data
}

func getInput(data []byte) Input {
	var grid [][]byte

	width, height, last := 0, 0, 0

	for i, b := range data {
		if b == '\n' {
			if width == 0 {
				width = i

				grid = make([][]byte, 0, width)
			}

			grid = append(grid, data[last:i])

			last = i + 1
			height++
		}
	}

	return Input{
		width:  width,
		height: height,
		data:   grid,
	}
}

func createCacheKeys(size, xat, yat, dirx, diry int) (string, string) {
	array1 := make([]string, size, size)
	array2 := make([]string, size, size)

	for i := 0; i < size; i++ {
		x := xat + (i * dirx)
		y := yat + (i * diry)

		key := fmt.Sprintf("%dx%d", x, y)

		array1[i] = key
		array2[size-i-1] = key
	}

	return strings.Join(array1, "|"), strings.Join(array2, "|")
}

func (in *Input) isOutOfBounds(x, y int) bool {
	return x < 0 || x >= in.width || y < 0 || y >= in.height
}

func (in *Input) findWord(cache map[string]struct{}, xat, yat, dirx, diry int) bool {
	letters := []byte{'X', 'M', 'A', 'S'}

	ak, bk := createCacheKeys(len(letters), xat, yat, dirx, diry)

	if _, ok := cache[ak]; ok {
		return false
	}

	if _, ok := cache[bk]; ok {
		return false
	}

	rightFound := 0
	inverseFound := 0

	for i := 0; i < len(letters); i += 1 {
		x := xat + (i * dirx)
		y := yat + (i * diry)

		if in.isOutOfBounds(x, y) {
			return false
		}

		if in.data[y][x] == letters[i] {
			rightFound++
		}

		if in.data[y][x] == letters[len(letters)-i-1] {
			inverseFound++
		}
	}

	cache[ak] = struct{}{}
	cache[bk] = struct{}{}

	return inverseFound == len(letters) || rightFound == len(letters)
}

func (in *Input) findCrossWord(x, y int) bool {
	topLeftX := x - 1
	topLeftY := y - 1
	topRightX := x + 1
	topRightY := y - 1

	bottomLeftX := x - 1
	bottomLeftY := y + 1
	bottomRightX := x + 1
	bottomRightY := y + 1

	if in.isOutOfBounds(topLeftX, topLeftY) {
		return false
	}

	if in.isOutOfBounds(topRightX, topRightY) {
		return false
	}

	if in.isOutOfBounds(bottomLeftX, bottomLeftY) {
		return false
	}

	if in.isOutOfBounds(bottomRightX, bottomRightY) {
		return false
	}

	if in.data[y][x] != 'A' {
		return false
	}

	at := in.data[topLeftY][topLeftX]
	ab := in.data[bottomRightY][bottomRightX]

	a := at == 'M' && ab == 'S' || at == 'S' && ab == 'M'

	bt := in.data[topRightY][topRightX]
	bb := in.data[bottomLeftY][bottomLeftX]

	b := bt == 'M' && bb == 'S' || bt == 'S' && bb == 'M'

	return a && b
}

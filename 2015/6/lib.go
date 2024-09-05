package main

import (
	"os"
	"strings"
)

type handler func(line string) bool

type LinesReader interface {
	Read(h handler)
}

type linesReader struct {
	filepath string
}

type fakeReader struct {
	lines []string
}

func NewFakeReader(lines []string) *fakeReader {
	return &fakeReader{
		lines: lines,
	}
}

func (fr *fakeReader) Read(h handler) {
	for _, line := range fr.lines {
		if h(line) {
			break
		}
	}
}

func NewReader(inputPath string) *linesReader {
	return &linesReader{
		filepath: inputPath,
	}
}

func (lr *linesReader) Read(h handler) {
	file, err := os.ReadFile(lr.filepath)

	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(file), "\n")

	if lines[len(lines)-1] == "" {
		lines = lines[:len(lines)-1]
	}

	for _, line := range lines {
		if h(line) {
			break
		}
	}
}

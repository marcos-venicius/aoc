package main

import (
	"log"
	"os"
	"strings"
)

func readLines() []string {
	data, err := os.ReadFile("./input.txt")

	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(data), "\n")

	return lines[:len(lines)-1]
}

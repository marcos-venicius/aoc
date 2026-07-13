package main

import (
  "fmt"
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

func startsWith5(h [16]byte) bool {
  return strings.HasPrefix(fmt.Sprintf("%x", h[:3]), "00000")
}

func startsWith6(h [16]byte) bool {
  return strings.HasPrefix(fmt.Sprintf("%x", h[:3]), "000000")
}

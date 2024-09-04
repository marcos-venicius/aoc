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

func isVowel(r rune) bool {
	switch r {
	case 'a', 'e', 'i', 'o', 'u':
		return true
	default:
		return false
	}
}

func isIlegal(a, b rune) bool {
	switch fmt.Sprintf("%c%c", a, b) {
	case "ab", "cd", "pq", "xy":
		return true
	default:
		return false
	}
}

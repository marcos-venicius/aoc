package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

type TachyonParticles struct {
	board [][]rune
	splitsAmount int
}

func main() {
	board := mountInitialBoard()

	tachyonParticles := TachyonParticles{
		board: board,
		splitsAmount: 0,
	}

	x, y := getInitialTachyonPosition(board)

	tachyonParticles.travelTachyon(x, y)

	fmt.Printf("P1: %d\n", tachyonParticles.splitsAmount)
}

func (t *TachyonParticles) travelTachyon(startX, startY int) {
	if startX < 0 || startY < 0 {
		return
	}

	if startY >= len(t.board) || startX >= len(t.board[startY]){
		return
	}

	if t.board[startY][startX] != '.' && t.board[startY][startX] != 'S' {
		return
	}

	for i := range (len(t.board) - startY - 1) {
		y := startY + i

		if t.board[y][startX] == '^' {
			t.splitsAmount += 1

			t.board[y][startX] = '@'

			t.travelTachyon(startX - 1, y)
			t.travelTachyon(startX + 1, y)

			break
		} else if t.board[y][startX] != 'S' {
			if t.board[y][startX] != '.' {
				break
			}

			t.board[y][startX] = '|'
		}
	}
}

func mountInitialBoard() [][]rune {
	filename := "./test.txt"

	if len(os.Args) == 2 {
		filename = os.Args[1]
	}

	data, err := os.ReadFile(filename)

	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(data), "\n")

	board := make([][]rune, 0)

	for _, line := range lines {
		row := make([]rune, 0)

		for _, c := range line {
			row = append(row, c)
		}

		board = append(board, row)
	}

	return board
}

func getInitialTachyonPosition(board [][]rune) (int, int) {
	for y := range len(board) {
		for x := range len(board[y]) {
			if board[y][x] == 'S' {
				return x, y
			}
		}
	}

	log.Fatal("could not find initial tachyon position")

	return 0, 0
}

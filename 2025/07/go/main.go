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
	partTwo := resolvePartTwo(x, y, board)

	fmt.Printf("P1: %d\n", tachyonParticles.splitsAmount)
	fmt.Printf("P2: %d\n", partTwo)
}

func resolvePartTwo(startX, startY int, board [][]rune) int {
	dp := make([][]int, len(board))

	for i, row := range board {
		dp[i] = make([]int, len(row))
	}

	dp[startY][startX] = 1

	for y := startY + 1; y < len(board); y++ {
		for x := 0; x < len(board[y]); x++ {
			if board[y][x] == '@' {
				if board[y-1][x] == '|' {
					dp[y][x] = dp[y-1][x]
				}

				continue
			}

			if board[y-1][x] == '|' || board[y-1][x] == 'S' {
				dp[y][x] += dp[y-1][x]
			}

			if x > 0 && board[y-1][x-1] == '@' {
				dp[y][x] += dp[y-1][x-1]
			}

			if x < len(board[y]) - 1 && board[y-1][x+1] == '@' {
				dp[y][x] += dp[y-1][x+1]
			}
		}
	}

	lastRow := len(dp) - 1
	count := 0

	for i := 0; i < len(dp[lastRow]); i++ {
		count += dp[lastRow][i]
	}

	return count
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

	for i := range (len(t.board) - startY) {
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

		if len(row) > 0 {
			board = append(board, row)
		}
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

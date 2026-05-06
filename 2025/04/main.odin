package main

import "core:os"
import "core:fmt"
import "core:strings"

Board :: [dynamic][dynamic]ObjectKind
ObjectKind :: enum {
  PaperRoll = '@',
  Empty = '.'
}

POSITIONS :: [8][2]int{{-1, -1}, {0, -1}, {1, -1}, {1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}}

main :: proc() {
  if len(os.args) != 2 {
    fmt.fprintf(os.stderr, "usage: %s <input file>\n", os.args[0])
    os.exit(1)
  }

  // TODO: refactor this to do proper memory management. It's working, but it's good to learn more about odin
  // TODO: add a visualization with raylib. I think it would be very fun

  board := read_input(os.args[1])

  part_one, _ := execute_solution(board)
  part_two, new_board := execute_solution(board)

  for true {
    result := 0

    result, new_board = execute_solution(new_board)

    if result == 0 {
      break
    }

    part_two += result
  }

  fmt.printf("P1: %d\n", part_one)
  fmt.printf("P2: %d\n", part_two)
}

execute_solution :: proc(board: Board) -> (int, Board) {
  answer := 0

  output := deep_copy(board)

  for y in 0..<len(board) {
    for x in 0..<len(board[y]) {
      if board[y][x] != .PaperRoll {
        continue
      }

      paper_rolls := 0

      for p in POSITIONS {
        dx := p[0]
        dy := p[1]

        cx := x + dx
        cy := y + dy

        if cx < 0 || cx >= len(board[y]) || cy < 0 || cy >= len(board) {
          continue
        }

        if board[cy][cx] == .PaperRoll {
          paper_rolls += 1
        }

        if paper_rolls >= 4 {
          break
        }
      }

      if paper_rolls < 4 {
        answer += 1
        output[y][x] = .Empty
      }
    }
  }

  return answer, output
}

deep_copy :: proc(board: Board) -> Board {
  kopy := make(Board, len(board))

  for i in 0..<len(board) {
    kopy[i] = make([dynamic]ObjectKind, len(board[i]))

    copy(kopy[i][:], board[i][:])
  }

  return kopy
}

read_input :: proc(filename: string) -> Board {
  data, err := os.read_entire_file(filename, context.allocator)

  if err != nil {
    fmt.fprintf(os.stderr, "could not read %s\n", filename)
    os.exit(1)
  }

  defer delete(data, context.allocator)

  board: Board

  it := string(data)

  for line in strings.split_lines_iterator(&it) {
    row: [dynamic]ObjectKind

    for char in line {
      switch char {
      case '@': append(&row, ObjectKind.PaperRoll)
      case '.': append(&row, ObjectKind.Empty)
      case:
        fmt.fprintf(os.stderr, "unreacheable: invalid character '%c'\n", char)
        os.exit(1)
      }
    }

    append(&board, row)
  }

  return board
}

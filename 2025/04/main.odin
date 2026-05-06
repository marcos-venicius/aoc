package main

import "core:os"
import "core:fmt"
import "core:strings"

main :: proc() {
  if len(os.args) != 2 {
    fmt.fprintf(os.stderr, "usage: %s <input file>\n", os.args[0])
    os.exit(1)
  }

  board := read_input(os.args[1])

  defer delete(board)

  part_one := execute_part_one(board)

  fmt.printf("P1: %d\n", part_one)
  fmt.printf("P2: X\n")
}

execute_part_one :: proc(board: [dynamic][dynamic]ObjectKind) -> int {
  answer := 0

  POSITIONS :: [8][2]int{{-1, -1}, {0, -1}, {1, -1}, {1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}}

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
      }

      if paper_rolls < 4 {
        answer += 1
      }
    }
  }

  return answer
}

ObjectKind :: enum {
  PaperRoll = '@',
  Empty = '.'
}

read_input :: proc(filename: string) -> [dynamic][dynamic]ObjectKind {
  data, err := os.read_entire_file(filename, context.allocator)

  if err != nil {
    fmt.fprintf(os.stderr, "could not read %s\n", filename)
    os.exit(1)
  }

  defer delete(data, context.allocator)

  board: [dynamic][dynamic]ObjectKind

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

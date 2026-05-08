package main

import rl "vendor:raylib"

Block :: struct {
  x, y, h, w: i32,
  color: rl.Color,
  done: bool
}

WindowBoard :: [dynamic][dynamic]Block

main_visualize :: proc(board: Board) {
  _, render_pipeline := create_render_pipeline(board)

  PADDING :: 20

  rl.InitWindow(0, 0, "AOC DAY 04 VISUALIZATION")

  screen_width := rl.GetScreenWidth()
  screen_height := rl.GetScreenHeight()
  rows := i32(len(board))
  cols := i32(len(board[0]))

  available_width := i32(f32(screen_width) * 0.8)
  available_height := i32(f32(screen_height) * 0.8)

  cell_width := i32(available_width / cols)
  cell_height := i32(available_height / rows)

  if cell_width > 20 {
    cell_width = 20
  }

  if cell_height > 20 {
    cell_height = 20
  }

  W_WIDTH := i32(cell_width * cols + PADDING * 2)
  W_HEIGHT := i32(cell_height * rows + PADDING * 2)

  center_x := (screen_width - W_WIDTH) / 2
  center_y := (screen_height - W_HEIGHT) / 2

  rl.SetWindowPosition(center_x, center_y)
  rl.SetWindowSize(W_WIDTH, W_HEIGHT)

  rl.SetTargetFPS(60)

  window: WindowBoard

  for row, i in board {
    blocks: [dynamic]Block

    for cell, j in row {
      x := i32(PADDING + (cell_width * i32(j)))
      y := i32(PADDING + (cell_height * i32(i)))

      if cell == .Empty {
        append(&blocks, Block{ x = x, y = y, h = cell_height, w = cell_width, color = { 73, 73, 73, 255 }})
      } else if cell == .PaperRoll {
        append(&blocks, Block{ x = x, y = y, h = cell_height, w = cell_width, color = { 208, 191, 143, 255 }})
      }
    }

    append(&window, blocks)
  }

  render_step := 0

  for !rl.WindowShouldClose() {
    if rl.IsKeyPressed(.Q) {
      break
    }

    if render_step < len(render_pipeline) {
      step := render_pipeline[render_step]

      if step.done {
        window[step.y][step.x].done = true
      }

      block := window[step.y][step.x]

      if !block.done || (block.done && step.done) {
        x := i32(PADDING + (cell_width * i32(step.x)))
        y := i32(PADDING + (cell_height * i32(step.y)))

        window[step.y][step.x].color = step.color
      }

      render_step += 1
    }

    rl.BeginDrawing()

    rl.ClearBackground(BG_COLOR)

    for row in window {
      for block in row {
        rl.DrawRectangle(block.x, block.y, block.w, block.h, block.color)
      }
    }

    rl.EndDrawing()
  }

  rl.CloseWindow()
}

RenderStep :: struct {
  color: rl.Color,
  x, y: int,
  done: bool
}

BG_COLOR          :: rl.Color{ 20, 20, 20, 255 }
WALK_COLOR        :: rl.Color{ 250, 254, 255, 255 }
SET_COLOR         :: rl.Color{ 255, 255, 255, 255 }
EMPTY_COLOR       :: rl.Color{ 73, 73, 73, 255 }
PAPER_ROLL_COLOR  :: rl.Color{ 208, 191, 143, 255 }
HIT_COLOR         :: rl.Color{ 255, 125, 25, 255 }
MATCH_COLOR       :: rl.Color{ 13, 255, 0, 255 }
SUCCESS_COLOR     :: rl.Color{ 0, 213, 255, 255 }
ERROR_COLOR       :: rl.Color{ 255, 0, 0, 255 }
GREEN_COLOR       :: rl.Color{ 0, 255, 34, 255 }

create_render_pipeline :: proc(board: Board) -> (Board, [dynamic]RenderStep) {
  answer := 0

  output := deep_copy(board)

  render_pipeline: [dynamic]RenderStep

  for y in 0..<len(board) {
    for x in 0..<len(board[y]) {
      append(&render_pipeline, RenderStep{ x = x, y = y, color = WALK_COLOR })

      if board[y][x] != .PaperRoll {
        append(&render_pipeline, RenderStep{ x = x, y = y, color = EMPTY_COLOR })
        continue
      }

      append(&render_pipeline, RenderStep{ x = x, y = y, color = SET_COLOR })

      paper_rolls := 0

      for p in POSITIONS {
        dx := p[0]
        dy := p[1]

        cx := x + dx
        cy := y + dy

        if cx < 0 || cx >= len(board[y]) || cy < 0 || cy >= len(board) {
          continue
        }

        append(&render_pipeline, RenderStep{ x = cx, y = cy, color = HIT_COLOR })

        if board[cy][cx] == .PaperRoll {
          append(&render_pipeline, RenderStep{ x = cx, y = cy, color = MATCH_COLOR })
          append(&render_pipeline, RenderStep{ x = cx, y = cy, color = PAPER_ROLL_COLOR })
          paper_rolls += 1
        } else {
          append(&render_pipeline, RenderStep{ x = cx, y = cy, color = EMPTY_COLOR })
        }

        if paper_rolls >= 4 {
          break
        }
      }

      if paper_rolls < 4 {
        answer += 1
        output[y][x] = .Empty
        append(&render_pipeline, RenderStep{ x = x, y = y, color = SUCCESS_COLOR })
        append(&render_pipeline, RenderStep{ x = x, y = y, color = SUCCESS_COLOR, done = true })
      } else {
        append(&render_pipeline, RenderStep{ x = x, y = y, color = ERROR_COLOR })
        append(&render_pipeline, RenderStep{ x = x, y = y, color = PAPER_ROLL_COLOR })
      }
    }
  }

  for y in 0..<len(board) {
    for x in 0..<len(board[y]) {
      if board[y][x] == output[y][x] {
        append(&render_pipeline, RenderStep{ x = x, y = y, color = BG_COLOR, done = true })
      } else {
        append(&render_pipeline, RenderStep{ x = x, y = y, color = GREEN_COLOR, done = true })
      }
    }
  }

  return output, render_pipeline
}

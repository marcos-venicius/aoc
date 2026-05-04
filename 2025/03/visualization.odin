package main

import "core:os"
import "core:fmt"
import "core:strings"
import rl "vendor:raylib"

BatteryJoltage :: struct {
  as_rune:  rune,
  as_int:   int
}

Object :: struct {
  x, y, w, h: i32,
  color:      rl.Color
}

Value :: struct {
  x, y:     f32,
  as_rune:  rune,
  as_int:   int
}

Track :: struct {
  object:     Object,
  slots:      [dynamic]Object,
  batteries:  [dynamic]Object,
  values:     [dynamic]Value,
}

RenderOperationKind :: enum {
  SelectBattery,
  MoveBattery,
  Finish
}

RenderOperation :: struct {
  kind: RenderOperationKind,

  track_index, battery_index, slot_index: int
}

read_input :: proc(filepath: string) -> [dynamic][dynamic]BatteryJoltage {
  data, err := os.read_entire_file(filepath, context.allocator)

  if err != nil {
    fmt.printf("could not read input file %s\n", filepath)
    os.exit(1)
  }

  defer delete(data, context.allocator)

  it := string(data)

  lines: [dynamic][dynamic]BatteryJoltage

  for line in strings.split_lines_iterator(&it) {
    if len(line) == 0 {
      continue
    }

    numbers: [dynamic]BatteryJoltage

    for i in 0..<len(line) {
      n: int = int(line[i] - '0')

      append(&numbers, BatteryJoltage{rune(line[i]), n})
    }

    append(&lines, numbers)
  }

  return lines
}

main :: proc() {
  lines := read_input("./test.txt")

  tracks: [dynamic]Track
  render_operations: [dynamic]RenderOperation

  defer delete(lines)
  defer delete(tracks)
  defer delete(render_operations)

  OBJECT_WIDTH    :: 20
  OBJECT_HEIGHT   :: 20
  PADDING         :: 20
  FONT_SIZE       :: 20
  BATTERIES_COUNT :: 12

  WIDTH   := len(lines[0]) * OBJECT_WIDTH * 2 + PADDING * 2
  HEIGHT  := 480

  // populate the board with initial values

  {
    y := i32((HEIGHT / 2) - (((OBJECT_HEIGHT + PADDING) * len(lines)) / 2))

    for line, i in lines {
      line_width := WIDTH - (PADDING * 2)
      line_length := len(line)

      track := Track{
        object = Object{
          x = PADDING,
          y = y,

          w = i32(line_width),
          h = i32(OBJECT_HEIGHT),

          color = { 73, 73, 73, 255 }
        }
      }

      xjump := (line_width / (line_length - 1))
      x := PADDING

      for number, j in line {
        slot := Object{
          x = i32(x),
          y = y,

          w = OBJECT_WIDTH,
          h = OBJECT_HEIGHT,

          color = { 92, 136, 139, 255 }
        }

        value := Value{
          x = f32(x + OBJECT_WIDTH / 4),
          y = f32(y),

          as_rune = number.as_rune,
          as_int = number.as_int
        }

        append(&track.slots, slot)
        append(&track.values, value)

        x += xjump
      }

      batteries_start := len(line) - BATTERIES_COUNT
      batteries_end := len(line)

      for i in batteries_start..<batteries_end {
        battery := Object{
          x = track.slots[i].x,
          y = track.slots[i].y,

          w = track.slots[i].w,
          h = track.slots[i].h,

          color = { 208, 191, 143, 255 }
        }

        append(&track.batteries, battery)
      }

      append(&tracks, track)

      y += OBJECT_HEIGHT + PADDING
    }
  }

  // create render operations

  {
    for track, track_index in tracks {
      size := len(track.slots)
      robots_done := 0
      robots_walking := BATTERIES_COUNT
      indexes: [dynamic]int

      defer delete(indexes)

      for robots_done < BATTERIES_COUNT {
        left_most := indexes[len(indexes) - 1] + 1 if len(indexes) > 0 else 0
        right_most := size - robots_walking + 1
        battery_index := robots_done

        append(&render_operations, RenderOperation{
          kind = .SelectBattery,
          battery_index = battery_index,
          track_index = track_index
        })

        max_number_index := left_most

        append(&render_operations, RenderOperation{
          kind = .MoveBattery,

          battery_index = battery_index,
          slot_index = left_most,
          track_index = track_index
        })

        for i in left_most..<right_most {
          append(&render_operations, RenderOperation{
            kind = .MoveBattery,

            battery_index = battery_index,
            slot_index = i,
            track_index = track_index
          })

          if track.values[i].as_int > track.values[max_number_index].as_int {
            max_number_index = i

            append(&render_operations, RenderOperation{
              kind = .MoveBattery,

              battery_index = battery_index,
              slot_index = i,
              track_index = track_index
            })
          }
        }

        append(&render_operations, RenderOperation{
          kind = .MoveBattery,

          battery_index = battery_index,
          slot_index = max_number_index,
          track_index = track_index
        })

        append(&render_operations, RenderOperation{
          kind = .Finish,

          battery_index = battery_index,
          track_index = track_index
        })

        append(&indexes, max_number_index)

        robots_walking -= 1
        robots_done += 1
      }
    }
  }

  // rendering
  rl.InitWindow(i32(WIDTH), i32(HEIGHT), "AOC DAY 03 VISUALIZATION")

  rl.SetTargetFPS(144)

  default_font := rl.GetFontDefault()

  operation_index := 0

  selected_battery_color := rl.Color{ 172, 115, 115, 255 }
  default_battery_color := rl.Color{ 208, 191, 143, 255 }
  finish_battery_color := rl.Color{ 127, 159, 127, 255 }

  display := false

  for !rl.WindowShouldClose() {
    if rl.IsKeyPressed(.Q) {
      break
    }

    if display == false {
      if rl.IsKeyPressed(.ENTER) {
        rl.SetTargetFPS(5)
        display = true
      }

      rl.BeginDrawing()
      rl.ClearBackground({ 20, 20, 20, 255 })
      rl.EndDrawing()
      continue
    }

    // update track state
    if operation_index < len(render_operations) {
      operation := render_operations[operation_index]

      if operation.kind == .SelectBattery {
        tracks[operation.track_index].batteries[operation.battery_index].color = selected_battery_color

        operation_index += 1
      } else if operation.kind == .MoveBattery {
        battery_x := tracks[operation.track_index].batteries[operation.battery_index].x
        slot_x := tracks[operation.track_index].slots[operation.slot_index].x

        if battery_x != slot_x {
          tracks[operation.track_index].batteries[operation.battery_index].x = slot_x
        }
      } else if operation.kind == .Finish {
        tracks[operation.track_index].batteries[operation.battery_index].color = finish_battery_color
      }

      operation_index += 1
    }

    // rendering objects
    rl.BeginDrawing()

    rl.ClearBackground({ 20, 20, 20, 255 })

    for track in tracks {
      rl.DrawRectangle(
        track.object.x,
        track.object.y,
        track.object.w,
        track.object.h,
        track.object.color
      )

      for slot in track.slots {
        rl.DrawRectangle(
          slot.x,
          slot.y,
          slot.w,
          slot.h,
          slot.color
        )
      }

      for battery in track.batteries {
        rl.DrawRectangle(
          battery.x,
          battery.y,
          battery.w,
          battery.h,
          battery.color
        )
      }

      for value in track.values {
        rl.DrawTextCodepoint(
          default_font,
          value.as_rune,
          {value.x, value.y},
          FONT_SIZE,
          { 0, 0, 0, 255}
        )
      }
    }

    rl.EndDrawing()
  }

  rl.CloseWindow()
}

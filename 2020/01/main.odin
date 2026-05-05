package main

import "core:os"
import "core:fmt"
import "core:strings"
import "core:strconv"

main :: proc() {
  if len(os.args) != 2 {
    fmt.printf("usage: %s <input file>\n", os.args[0])

    os.exit(1)
  }

  input := read_input(os.args[1])

  defer delete(input)

  part_one := exec_part_one(input)
  part_two := exec_part_two(input)

  fmt.printf("P1: %d\n", part_one)
  fmt.printf("P2: %d\n", part_two)
}

exec_part_one :: proc(input: [dynamic]int) -> int {
  for i in 0..<len(input) {
    for j in 0..<len(input) {
      if i == j {
        continue
      }

      if input[i] + input[j] == 2020 {
        return input[i] * input[j]
      }
    }
  }

  return 0
}

exec_part_two :: proc(input: [dynamic]int) -> int {
  for i in 0..<len(input) {
    for j in 0..<len(input) {
      if i == j {
        continue
      }
      for k in 0..<len(input) {
        if k == j {
          continue
        }

        if input[i] + input[j] + input[k] == 2020 {
          return input[i] * input[j] * input[k]
        }
      }
    }
  }

  return 0
}

read_input :: proc(filepath: string) -> [dynamic]int {
  data, err := os.read_entire_file(os.args[1], context.allocator)

  if err != nil {
    fmt.printf("%+v\n", err)
    os.exit(1)
  }

  defer delete(data, context.allocator)

  input: [dynamic]int

  it := string(data)

  for line in strings.split_lines_iterator(&it) {
    value, ok := strconv.parse_int(line)

    if !ok {
      fmt.printf("could not parse '%s' as integer\n", line)
      os.exit(1)
    }

    append(&input, value)
  }

  return input
}

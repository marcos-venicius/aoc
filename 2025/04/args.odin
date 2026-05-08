package main

import "core:os"
import "core:fmt"

CmdArguments :: struct {
  visualize: bool,
  input_filepath: string
}

parse_command_line_arguments :: proc() -> CmdArguments {
  args: CmdArguments

  help := false
  input_filepath: Maybe(string) = nil

  arg_index := 1 // skip program name

  for true {
    arg := shift(&arg_index)

    if arg == nil {
      break
    }

    switch arg.(string) {
    case "--visualize":
      args.visualize = true
    case "--help":
      help = true
    case:
      input_filepath = arg.(string)
      args.input_filepath = arg.(string)
    }
  }

  if help {
    fmt.fprintf(os.stdout, "usage: %s <input file> [flags]\n", os.args[0])
    fmt.fprintf(os.stdout, "\n")
    fmt.fprintf(os.stdout, "    --visualize        visualize the solution\n")
    fmt.fprintf(os.stdout, "    --help             show this help message\n")
    os.exit(0)
  }

  if input_filepath == nil {
    fmt.fprintf(os.stderr, "usage: %s <input file> [flags]\n", os.args[0])
    fmt.fprintf(os.stderr, "\n")
    fmt.fprintf(os.stderr, "    --visualize        visualize the solution\n")
    fmt.fprintf(os.stderr, "    --help             show this help message\n")
    os.exit(1)
  }

  return args
}

shift :: proc(arg_index: ^int) -> Maybe(string) {
  if arg_index^ >= len(os.args) {
    return nil
  }

  arg_index^ = arg_index^ + 1

  return os.args[arg_index^ - 1]
}

package main

import "fmt"

const CHAIN_SIZE = 10

type Input struct {
	grid [][]int
  chains [][CHAIN_SIZE]Vec2
}

type Vec2 struct {
  x, y int
}

func CreateInput() Input {
  return Input{
  	grid: make([][]int, 0),
    chains: make([][CHAIN_SIZE]Vec2, 0),
  }
}

func (in *Input) parseLine(line string) {
	row := make([]int, 0)

	for _, char := range line {
    row = append(row, int(char - '0'))
	}

  in.grid = append(in.grid, row)
}

func (in *Input) getChains(chain [CHAIN_SIZE]Vec2, x, y, next int) {
  if in.grid[y][x] != next {
    return
  }

  chain[next] = Vec2{ x: x, y: y }

  if in.grid[y][x] == 9 {
    in.chains = append(in.chains, chain)

    return
  }

  next++

  if (x - 1 >= 0) {
    in.getChains(chain, x - 1, y, next)
  }

  if (x + 1 < len(in.grid[y])) {
    in.getChains(chain, x + 1, y, next)
  }

  if (y - 1 >= 0) {
    in.getChains(chain, x, y - 1, next)
  }

  if (y + 1 < len(in.grid)) {
    in.getChains(chain, x, y + 1, next)
  }
}

func (in *Input) findChains() int {
  for y := 0; y < len(in.grid); y++ {
    for x := 0; x < len(in.grid); x++ {
      v := in.grid[y][x]

      if v == 0 {
        in.getChains([CHAIN_SIZE]Vec2{}, x, y, 0)
      }
    }
  }

  return len(in.chains)
}

func (in *Input) distinct() int {
  m := make(map[string]int)

  for _, chain := range in.chains {
    head := chain[0]
    tail := chain[CHAIN_SIZE - 1]
    key := fmt.Sprintf("%d-%d-%d-%d", head.x, head.y, tail.x, tail.y)

    m[key]++
  }

  return len(m)
}

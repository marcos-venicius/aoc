package main

import (
	"fmt"
	"os"
	"strconv"
)

type Block struct {
	id    int
	files int
}

type Blocks *[]*Block

func unwrap[T any](value T, err error) T {
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s", err.Error())
		os.Exit(1)
	}

	return value
}

func parseBlocks(line string, fragment bool) Blocks {
	blocks := make([]*Block, 0)

	blockID := 0

	for i := 0; i < len(line); i += 2 {
		files := unwrap(strconv.Atoi(line[i : i+1]))
		freeSpace := 0

		if i+1 < len(line) {
			freeSpace = unwrap(strconv.Atoi(line[i+1 : i+2]))
		}

		block := Block{id: blockID, files: files}

		if fragment {
			for j := 0; j < files; j++ {
				blocks = append(blocks, &block)
			}
		} else {
			blocks = append(blocks, &block)
		}

		for j := 0; j < freeSpace; j++ {
			blocks = append(blocks, nil)
		}

		blockID++
	}

	return &blocks
}

func rearrangeFragmentedBlocks(blocks Blocks) {
  b := *blocks

	l, r := 0, len(b)-1

	for l < r {
		for b[l] != nil {
			l++
		}

		for b[r] == nil {
			r--
		}

		if l < r {
			b[l], b[r] = b[r], b[l]
		}
	}
}

func checksumFragmentedBlocks(blocks Blocks) int64 {
	sum := int64(0)

	for i, block := range *blocks {
		if block == nil {
			continue
		}

		sum += int64(i) * int64(block.id)
	}

	return sum
}

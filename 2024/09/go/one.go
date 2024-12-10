package main

import (
	"fmt"
	"strconv"

	"github.com/marcos-venicius/aocreader"
)

type Block struct {
	id int
}

func parseBlocks(line string) []*Block {
	blocks := make([]*Block, 0)

	blockID := 0

	for i := 0; i < len(line); i += 2 {
		files := unwrap(strconv.Atoi(line[i : i+1]))
		freeSpace := 0

		if i+1 < len(line) {
			freeSpace = unwrap(strconv.Atoi(line[i+1 : i+2]))
		}

		for j := 0; j < files; j++ {
			block := &Block{id: blockID}

			blocks = append(blocks, block)
		}

		for j := 0; j < freeSpace; j++ {
			blocks = append(blocks, nil)
		}

		blockID++
	}

	return blocks
}

func rearrangeBlocks(blocks []*Block) []*Block {
	l, r := 0, len(blocks)-1

	for l < r {
		for blocks[l] != nil {
			l++
		}

		for blocks[r] == nil {
			r--
		}

		if l < r {
			blocks[l], blocks[r] = blocks[r], blocks[l]
		}
	}

	return blocks
}

func checksum(blocks []*Block) int64 {
	sum := int64(0)

	for i, block := range blocks {
		if block == nil {
			continue
		}

		sum += int64(i) * int64(block.id)
	}

	return sum
}

func solveOne(reader aocreader.LinesReader) int64 {
	_, line := reader.Line()

	blocks := parseBlocks(line)

	blocks = rearrangeBlocks(blocks)

	ans := checksum(blocks)

	fmt.Printf("01: %d\n", ans)

	return ans
}

package main

import (
	"fmt"
	"os"
	"strconv"
)

type Block struct {
	id int
}

type Blocks *[]Block

func Print(blocks Blocks) {
	for _, block := range *blocks {
		if block.isnil() {
			fmt.Printf(".")
		} else {
			fmt.Printf("%d", block.id)
		}
	}

	fmt.Println()
}

func (b Block) isnil() bool {
	return b.id == -1
}

func unwrap[T any](value T, err error) T {
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s", err.Error())
		os.Exit(1)
	}

	return value
}

func parseBlocks(line string) Blocks {
	blocks := make([]Block, 0)

	blockID := 0

	for i := 0; i < len(line); i += 2 {
		files := unwrap(strconv.Atoi(line[i : i+1]))
		freeSpace := 0

		if i+1 < len(line) {
			freeSpace = unwrap(strconv.Atoi(line[i+1 : i+2]))
		}

		block := Block{id: blockID}

		for j := 0; j < files; j++ {
			blocks = append(blocks, block)
		}

		for j := 0; j < freeSpace; j++ {
			blocks = append(blocks, Block{id: -1})
		}

		blockID++
	}

	return &blocks
}

func rearrangeFragmentedBlocks(blocks Blocks) {
	b := *blocks

	l, r := 0, len(b)-1

	for l < r {
		for !b[l].isnil() {
			l++
		}

		for b[r].isnil() {
			r--
		}

		if l >= r {
			break
		}

		b[l], b[r] = b[r], b[l]
	}
}

func swap(blocks Blocks, x1, x2, w int) {
	for i := 0; i < w; i++ {
		(*blocks)[x1+i], (*blocks)[x2+i] = (*blocks)[x2+i], (*blocks)[x1+i]
	}
}

func rearrangeBlocks(blocks Blocks) {
	b := *blocks

	r := len(b) - 1

	for r >= 0 {
		for r >= 0 && b[r].isnil() {
			r--
		}

		start := r

		for start >= 0 && b[start].id == b[r].id {
			start--
		}

		start++
		r++

		i := 0
		for i < r {
			if b[i].isnil() {
				end := i

				for end < len(b) && b[end].isnil() {
					end++
				}

				if end-i >= r-start {
					swap(blocks, i, start, r-start)

					break
				}

				i = end
			} else {
				i++
			}
		}

		r = start - 1
	}
}

func checksumFragmentedBlocks(blocks Blocks) int64 {
	sum := int64(0)

	for i, block := range *blocks {
		if block.isnil() {
			continue
		}

		sum += int64(i) * int64(block.id)
	}

	return sum
}

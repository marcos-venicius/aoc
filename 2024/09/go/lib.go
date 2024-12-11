package main

import (
	"fmt"
	"os"
	"strconv"
)

type Id int64
type Ids *[]Id

func (id Id) isFreeSpace() bool {
	return id == -1
}

func unwrap[T any](value T, err error) T {
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s", err.Error())
		os.Exit(1)
	}

	return value
}

func parseIds(line string) Ids {
	ids := make([]Id, 0)

	id := Id(0)

	for i := 0; i < len(line); i += 2 {
		files := unwrap(strconv.Atoi(line[i : i+1]))
		freeSpace := 0

		for j := 0; j < files; j++ {
			ids = append(ids, id)
		}

		if i+1 < len(line) {
			freeSpace = unwrap(strconv.Atoi(line[i+1 : i+2]))
		}

		for j := 0; j < freeSpace; j++ {
			ids = append(ids, -1)
		}

		id++
	}

	return &ids
}

func rearrangeFragmentedIds(ids Ids) {
	dids := *ids

	l, r := 0, len(dids)-1

	for l < r {
		for !dids[l].isFreeSpace() {
			l++
		}

		for dids[r].isFreeSpace() {
			r--
		}

		if l >= r {
			break
		}

		dids[l], dids[r] = dids[r], dids[l]
	}
}

func swap(ids Ids, x1, x2, w int) {
	for i := 0; i < w; i++ {
		(*ids)[x1+i], (*ids)[x2+i] = (*ids)[x2+i], (*ids)[x1+i]
	}
}

func rearrangeIdBlocks(ids Ids) {
	dids := *ids

	r := len(dids) - 1

	for r >= 0 {
		for r >= 0 && dids[r].isFreeSpace() {
			r--
		}

		start := r

		for start >= 0 && dids[start] == dids[r] {
			start--
		}

		start++
		r++

		i := 0

		for i < r {
			if dids[i].isFreeSpace() {
				end := i

				for end < len(dids) && dids[end].isFreeSpace() {
					end++
				}

				if end-i >= r-start {
					swap(ids, i, start, r-start)

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

func checksumIds(ids Ids) int64 {
	sum := Id(0)

	for i, id := range *ids {
		if id.isFreeSpace() {
			continue
		}

		sum += Id(i) * id
	}

	return int64(sum)
}

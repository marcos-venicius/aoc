package main

import "github.com/marcos-venicius/aocreader"

func solve(reader aocreader.LinesReader, windowSize int) int {
	ans := 0

	reader.Read(func(line string) bool {
		arr := make([]int, 26)

		l, r := 0, 1

		arr[line[l]%26] = 1

		for r-l < windowSize {
			if arr[line[r]%26] > 0 {
				arr[line[l]%26] = max(0, arr[line[l]%26]-1)
				l++
			} else {
				arr[line[r]%26]++
				r++
			}
		}

		ans = r

		return false
	})

	return ans
}

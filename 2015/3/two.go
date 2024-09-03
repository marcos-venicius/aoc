package main

import (
	"fmt"
)

func solveTwo(lines []string) {
	ans := 0

	line := lines[0]

	sx, sy, rx, ry, v := 0, 0, 0, 0, make(map[string]struct{})

	for index, m := range line {
		rm := index % 2
    
		if m == '^' && rm != 0 { sy-- }
		if m == '^' && rm == 0 { ry-- }
		if m == 'v' && rm != 0 { sy++ }
		if m == 'v' && rm == 0 { ry++ }
		if m == '>' && rm != 0 { sx++ }
		if m == '>' && rm == 0 { rx++ }
		if m == '<' && rm != 0 { sx-- }
		if m == '<' && rm == 0 { rx-- }

		p := fmt.Sprintf("%dx%d", sx, sy)

		if rm == 0 {
			p = fmt.Sprintf("%dx%d", rx, ry)
		}

		_, ok := v[p]

    v[p] = struct{}{}

		if !ok {
			ans++
		}
  }

	fmt.Printf("02: %d\n", ans)
}

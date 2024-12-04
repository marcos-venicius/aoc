package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBaseTwo(t *testing.T) {
  const text = `.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........`

  
	input := getInput([]byte(text))

  ans := solveTwo(input)

	assert.Equal(t, 9, ans)
}

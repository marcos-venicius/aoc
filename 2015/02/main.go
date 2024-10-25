package main

import (
  "fmt"
  "os"
  "log"
  "strings"
  "strconv"
  "math"
)

type dim struct {
  l int
  w int
  h int
}

func (d *dim) calcFeet() int {
  x := int(math.Min(math.Min(float64(d.l * d.w), float64(d.l * d.h)), float64(d.w * d.h)))

  return 2*d.l*d.w + 2*d.w*d.h + 2*d.h*d.l + x
}

func (d *dim) calcBowRibbon() int {
  one := 2 * (d.w + d.h)
  two := 2 * (d.l + d.h)
  three := 2 * (d.l + d.w)

  mind := int(math.Min(math.Min(float64(one), float64(two)), float64(three)))

  return mind + d.l * d.w * d.h
}

func lineToDim(line string) dim {
  split := strings.Split(line, "x")

  l, _ := strconv.Atoi(split[0])
  w, _ := strconv.Atoi(split[1])
  h, _ := strconv.Atoi(split[2])

  return dim{
    l: l,
    w: w,
    h: h,
  }
}

func readInput() []dim {
  data, err := os.ReadFile("./input.txt")

  if err != nil {
    log.Fatal(err)
  }

  chunks := strings.Split(string(data), "\n")

  var res []dim

  for _, c := range chunks {
    if c != "" {
      res = append(res, lineToDim(c))
    }
  }

  return res
}

func solve1() int {
  area := 0
  input := readInput()

  for _, d := range input {
    area += d.calcFeet()
  }

  return area
}

func solve2() int {
  area := 0
  input := readInput()

  for _, d := range input {
    area += d.calcBowRibbon()
  }

  return area
}

func main() {
  fmt.Println(solve1())
  fmt.Println(solve2())
}

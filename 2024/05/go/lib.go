package main

import (
	"regexp"
	"strconv"
)

type Input struct {
	parsingRules bool
	rules        map[int]map[int]struct{}
	updates      [][]int
	rulesRegex   *regexp.Regexp
	updatesRegex *regexp.Regexp
}

func CreateInput() Input {
	return Input{
		parsingRules: true,
		rules:        make(map[int]map[int]struct{}),
		updates:      make([][]int, 0),
		rulesRegex:   regexp.MustCompile(`(\d+)|(\d+)`),
		updatesRegex: regexp.MustCompile(`(\d+)`),
	}
}

func (in *Input) parseRule(line string) {
	rules := in.rulesRegex.FindAllString(line, -1)

	left, err := strconv.Atoi(rules[0])

	if err != nil {
		panic(err)
	}

	right, err := strconv.Atoi(rules[1])

	if err != nil {
		panic(err)
	}

	if _, ok := in.rules[left]; !ok {
		in.rules[left] = make(map[int]struct{})
	}

	in.rules[left][right] = struct{}{}
}

func (in *Input) parseUpdate(line string) {
	updates := in.updatesRegex.FindAllString(line, -1)

	slice := make([]int, 0)

	for _, update := range updates {
		value, err := strconv.Atoi(update)

		if err != nil {
			panic(err)
		}

		slice = append(slice, value)
	}

	in.updates = append(in.updates, slice)
}

func (in *Input) ParseLine(line string) {
	if line == "" {
		in.parsingRules = false

		return
	}

	if in.parsingRules {
		in.parseRule(line)
	} else {
		in.parseUpdate(line)
	}
}

func (in *Input) updateIsCorrect() bool {
	return true
}

func (in *Input) getCorrectUpdatesIndexes() []int {
	indexes := make([]int, 0)

	for i, line := range in.updates {
		valid := true
		for j, update := range line {
			for k := 0; k < j; k++ {
				if _, ok := in.rules[line[k]]; !ok {
					valid = false

					break
				}
				if _, ok := in.rules[line[k]][update]; !ok {
					valid = false

					break
				}
			}

			if !valid {
				break
			}
		}

		if valid {
			indexes = append(indexes, i)
		}
	}

	return indexes
}

func (in *Input) getIncorrectUpdatesIndexes() []int {
	indexes := make([]int, 0)

	for i, line := range in.updates {
		valid := true
		for j, update := range line {
			for k := 0; k < j; k++ {
				if _, ok := in.rules[line[k]]; !ok {
					valid = false

					break
				}
				if _, ok := in.rules[line[k]][update]; !ok {
					valid = false

					break
				}
			}

			if !valid {
				break
			}
		}

		if !valid {
			indexes = append(indexes, i)
		}
	}

	return indexes
}

func (in *Input) fixOrder(index int) {
	array := in.updates[index]

	for i, update := range array {
		for k := 0; k < i; k++ {
			if _, ok := in.rules[array[k]]; !ok {
				array[k], array[i] = array[i], array[k]

				in.fixOrder(index)
				return
			}

			if _, ok := in.rules[array[k]][update]; !ok {
				array[k], array[i] = array[i], array[k]

				in.fixOrder(index)
				return
			}
		}
	}
}

func (in *Input) fixUpdates(indexes []int) {
	for _, i := range indexes {
		in.fixOrder(i)
	}
}

func (in *Input) sumIndexes(indexes []int) (r int) {
	for _, i := range indexes {
		m := len(in.updates[i]) / 2

		r += in.updates[i][m]
	}

	return r
}

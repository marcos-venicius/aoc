package main

import (
	"regexp"
	"strconv"
)

type Expression struct {
	left  int
	right int
}

func toint(n string) int {
	v, err := strconv.Atoi(n)

	if err != nil {
		panic(err)
	}

	return v
}

func parseCompleteExpressions(line string, state bool) ([]Expression, bool) {
	expressions := make([]Expression, 0)

	regex := regexp.MustCompile(`(mul\((\d+),(\d+)\))|(don't\(\))|(do\(\))`)

	matches := regex.FindAllStringSubmatch(line, -1)

	enabled := state

	for _, match := range matches {
		switch match[0] {
		case "don't()":
			enabled = false
		case "do()":
			enabled = true
		default:
			if !enabled {
				break
			}

			left := toint(match[2])
			right := toint(match[3])

			expression := Expression{
				left:  left,
				right: right,
			}

			expressions = append(expressions, expression)
		}
	}

	return expressions, enabled
}

func parseExpressions(line string) []Expression {
	expressions := make([]Expression, 0)

	regex := regexp.MustCompile(`mul\((\d+),(\d+)\)`)

	matches := regex.FindAllStringSubmatch(line, -1)

	for _, match := range matches {
		left := toint(match[1])
		right := toint(match[2])

		expression := Expression{
			left:  left,
			right: right,
		}

		expressions = append(expressions, expression)
	}

	return expressions
}

func (e *Expression) evaluate() int {
	return e.left * e.right
}

func evaluateExpressions(expressions []Expression) int {
	sum := 0

	for _, expression := range expressions {
		sum += expression.evaluate()
	}

	return sum
}

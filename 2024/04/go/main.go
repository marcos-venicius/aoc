package main

func main() {
  content := readFile("../input.txt")
	input := getInput(content)

	solveOne(input)
	solveTwo(input)
}

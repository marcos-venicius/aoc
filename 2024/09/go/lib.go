package main

import (
	"fmt"
	"os"
)

func unwrap[T any](value T, err error) T {
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s", err.Error())
		os.Exit(1)
	}

	return value
}

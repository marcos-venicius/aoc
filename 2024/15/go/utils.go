package main

import "fmt"

type Vec2 struct {
	x, y int
}

func vec2(x, y int) Vec2 {
	return Vec2{
		x: x, y: y,
	}
}

func (v Vec2) Diff(of Vec2) Vec2 {
	return Vec2{
		x: of.x - v.x,
		y: of.y - v.y,
	}
}

func (v Vec2) Abs() Vec2 {
	out := Vec2{
		x: v.x,
		y: v.y,
	}

	if v.x < 0 {
		out.x = v.x * -1
	}

	if v.y < 0 {
		out.y = v.y * -1
	}

	return out
}

func (v Vec2) Sum(b Vec2) Vec2 {
	return Vec2{
		x: v.x + b.x,
		y: v.y + b.y,
	}
}

func (v Vec2) DecY(n int) Vec2 {
	return Vec2{
		x: v.x,
		y: v.y - n,
	}
}

func (v Vec2) IncY(n int) Vec2 {
	return Vec2{
		x: v.x,
		y: v.y + n,
	}
}

func (v Vec2) DecX(n int) Vec2 {
	return Vec2{
		x: v.x - n,
		y: v.y,
	}
}

func (v Vec2) IncX(n int) Vec2 {
	return Vec2{
		x: v.x + n,
		y: v.y,
	}
}

func ternary[T any](this T, when bool, orelse T) T {
	if when {
		return this
	}

	return orelse
}

func printf(format string, args ...any) {
	fmt.Printf(format, args...)
}

func printfn(format string, args ...any) {
	fmt.Printf(fmt.Sprintf("%s\n", format), args...)
}

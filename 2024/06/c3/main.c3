module aoc;

import std::io;
import std::collections::map;

const int SIZE = 130;

fault Errors {
  GUARD_POSITION_NOT_FOUND,
  INVALID_DIRECTION,
}

def Vector2 = int[<2>];

const TOP = Vector2{ 0, -1 };
const RIGHT = Vector2{ 1, 0 };
const LEFT = Vector2{ -1, 0 };
const BOTTOM = Vector2{ 0, 1 };

fn uint Vector2.hash(Vector2 v) {
  if (v.x > v.y) {
    return ((v.x + v.y) * (v.x + v.y + 1)) / 2 + v.y;
  } 

  return ((v.y + v.x) * (v.y + v.x + 1)) / 2 + v.x;
}

fn bool Vector2.equals(Vector2 a, Vector2 b) {
  return a.x == b.x && a.y == b.y;
}

def Map = HashMap(<Vector2, bool>);

fn void! Vector2.turnRight90degrees(Vector2* this) {
  switch (*this) {
    case TOP:
      this.x = 1;
      this.y = 0;
    case RIGHT:
      this.x = 0;
      this.y = 1;
    case BOTTOM:
      this.x = -1;
      this.y = 0;
    case LEFT:
      this.x = 0;
      this.y = -1;
    default:
      return Errors.INVALID_DIRECTION?;
  }
}

fn char[SIZE][SIZE]! readInput(String path) {
  char[SIZE][SIZE] data;

  File file = file::open(path, "r")!;

  defer (void)file.close();

  for (int y = 0; y < SIZE; y++) {
    for (int x = 0; x < SIZE; x++) {
      char b = file.read_byte()!;

      if (b == '\n') {
        b = file.read_byte()!;
      }

      data[y][x] = b;
    }
  }

  return data;
}

fn Vector2! getGuardPosition(char[SIZE][SIZE]* table) {
  for (int y = 0; y < SIZE; y++) {
    for (int x = 0; x < SIZE; x++) {
      if ((*table)[y][x] == '^') {
        return { x, y };
      }
    }
  }

  return Errors.GUARD_POSITION_NOT_FOUND?;
}

fn Vector2 Vector2.nextPosition(Vector2* v, Vector2* dir) {
  return {
    v.x + dir.x,
    v.y + dir.y,
  };
}

fn bool isOutOfBounds(Vector2* next) {
  return next.y < 0 || next.y >= SIZE || next.x < 0 || next.x >= SIZE;
}

fn bool isBlocked(char[SIZE][SIZE]* table, Vector2* pos) {
  return (*table)[pos.y][pos.x] == '#';
}

fn void! main() {
  char[SIZE][SIZE]! data = readInput("../input.txt");

  if (catch err = data) {
    io::printfn("could not read file due to: %s", err);
    return;
  }

  if (catch err = one(&data)) {
    io::printfn("one error: %s", err);
  }

  if (catch err = two(&data)) {
    io::printfn("two error: %s", err);
  }
}

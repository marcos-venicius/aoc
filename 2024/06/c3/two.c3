module aoc;

import std::io;
import std::collections::map;

fn bool! checkCycle(char[SIZE][SIZE]* data, Vector2 guard) {
  HashMap(<Vector2, int>) m;

  m.new_init();

  Vector2 dir = { 0, -1 };

  while (true) {
    Vector2 nextPosition = guard.nextPosition(&dir);

    if (isOutOfBounds(&nextPosition)) break;

    if (isBlocked(data, &nextPosition)) {
      int count = 0;

      if (m.has_key(guard)) {
        count = m.get(guard)!! + 1;
      } else {
        count = 1;
      }

      m.set(guard, count);

      if (count % 4 == 0) return true;

      dir.turnRight90degrees()!;
    } else {
      guard = nextPosition;
    }
  }

  return false;
}

fn void! two(char[SIZE][SIZE]* data) {
  Vector2 guard = getGuardPosition(data)!;

  int count = 0;
  
  foreach (y, chars : *data) {
    foreach (x, c : chars) {
      if (c == '#' || c == '^') continue;

      (*data)[y][x] = '#';

      if (checkCycle(data, guard)!) {
        count++;
      }

      (*data)[y][x] = c;
    }
  }

  io::printfn("02: %d", count);
}

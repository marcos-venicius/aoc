module aoc;

import std::io;

fn void! one(char[SIZE][SIZE]* data) {
  Vector2 guard = getGuardPosition(data)!;

  Vector2 dir = { 0, -1 };

  Map m;

  m.new_init();

  defer m.clear();

  while (true) {
    m.set(guard, true);

    Vector2 nextPosition = guard.nextPosition(&dir);

    if (isOutOfBounds(&nextPosition)) {
      break;
    }

    if (isBlocked(data, &nextPosition)) {
      dir.turnRight90degrees()!;
    } else {
      guard = nextPosition;
    }
  }

  usz walked = m.len();

  io::printfn("01: %d", walked);
}

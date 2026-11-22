use std::cmp::Ordering;
use std::collections::HashMap;
use std::time::Instant;
use std::{env, fs};

#[derive(Debug, Clone)]
enum Direction {
    Up,
    Down,
    Right,
    Left,
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct Pos {
    x: i32,
    y: i32,
}

impl Ord for Pos {
    fn cmp(&self, other: &Self) -> Ordering {
        let a = self.x.abs() + self.y.abs();
        let b = other.x.abs() + other.y.abs();

        if a < b {
            return Ordering::Less;
        }

        if a > b {
            return Ordering::Greater;
        }

        return Ordering::Equal;
    }
}

impl PartialOrd for Pos {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn get_input() -> (Vec<(Direction, i32)>, Vec<(Direction, i32)>) {
    let args: Vec<String> = env::args().collect();

    let input = if args.len() == 2 {
        args[1].clone()
    } else {
        "./test.txt".to_string()
    };

    let content = fs::read_to_string(input).expect("well, we failed");
    let lines: Vec<Vec<(Direction, i32)>> = content
        .lines()
        .map(|line| {
            line.split(',')
                .map(|chunk| {
                    (
                        match chunk.chars().nth(0) {
                            Some('U') => Direction::Up,
                            Some('D') => Direction::Down,
                            Some('R') => Direction::Right,
                            Some('L') => Direction::Left,
                            _ => panic!("Oh Jesus"),
                        },
                        chunk[1..].parse().expect("Here we go"),
                    )
                })
                .collect()
        })
        .collect();

    (lines[0].clone(), lines[1].clone())
}

fn expand_wire(wire: &Vec<(Direction, i32)>) -> HashMap<Pos, i32> {
    let mut board: HashMap<Pos, i32> = HashMap::new();

    let mut x = 0;
    let mut y = 0;
    let mut steps = 0;

    for (dir, units) in wire {
        let dx = match dir {
            Direction::Left => -1,
            Direction::Right => 1,
            _ => 0,
        };
        let dy = match dir {
            Direction::Up => -1,
            Direction::Down => 1,
            _ => 0,
        };

        for i in 1..=*units {
            x += dx;
            y += dy;

            board.insert(Pos { x, y }, steps + i);
        }

        steps += units
    }

    board
}

fn main() {
    let (wire_one, wire_two) = get_input();

    let start = Instant::now();

    let board_one = expand_wire(&wire_one);
    let board_two = expand_wire(&wire_two);

    let mut nearest_manhattan_distance = board_one.keys().collect::<Vec<&Pos>>();

    nearest_manhattan_distance.sort_by(|pos_one, pos_two| pos_one.cmp(pos_two));

    nearest_manhattan_distance = nearest_manhattan_distance
        .into_iter()
        .filter(|pos| board_two.contains_key(pos))
        .collect();

    let mut min_distance: Option<i32> = None;
    let mut min_steps: Option<i32> = None;

    for pos in nearest_manhattan_distance {
        let distance = pos.x.abs() + pos.y.abs();

        if min_distance.is_none() {
            min_distance = Some(distance);
        }

        let steps_sum = board_one[pos] + board_two[pos];

        if min_steps.is_none() {
            min_steps = Some(steps_sum);
        } else if steps_sum < min_steps.expect("Why aren't you valid?") {
            min_steps = Some(steps_sum);
        }
    }

    println!("P1: {}", min_distance.expect("Shoulda have a value"));
    println!("P2: {}", min_steps.expect("Shoulda have a value"));

    let duration = start.elapsed();

    println!("exec time: {:.3}s", duration.as_secs_f64());
}

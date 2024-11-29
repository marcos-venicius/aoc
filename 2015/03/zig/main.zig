const one = @import("./one.zig").one;
const two = @import("./two.zig").two;

pub fn main() !void {
    try one();
    try two();
}

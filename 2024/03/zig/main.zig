const std = @import("std");
const one = @import("./one.zig").one;

pub fn main() !void {
    const result = try one();

    std.debug.print("01: {d}\n", .{result});
}

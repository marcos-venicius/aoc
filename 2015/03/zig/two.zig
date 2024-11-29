const std = @import("std");
const Vector2 = @import("./lib.zig").Vector2;

pub fn two() !void {
    var ans: i32 = 0;

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var board = std.AutoHashMap(Vector2, bool).init(allocator);
    defer board.deinit();

    var file = try std.fs.cwd().openFile("./input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var elf = Vector2{};
    var santa = Vector2{};
    var curr: *Vector2 = undefined;
    var i: i32 = 0;

    while (true) : (i += 1) {
        const char = in_stream.readByte() catch break;

        curr = if (@mod(i, 2) == 0) &santa else &elf;

        if (!board.contains(curr.*)) ans += 1;

        try board.put(curr.*, true);

        switch (char) {
            '>' => curr.xright(),
            '<' => curr.xleft(),
            'v' => curr.ydown(),
            '^' => curr.yup(),
            '\n' => break,
            else => unreachable,
        }
    }

    std.debug.print("02: {}\n", .{ans});
}

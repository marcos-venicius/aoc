const std = @import("std");
const Vector2 = @import("./lib.zig").Vector2;

pub fn one() !void {
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

    var pos = Vector2{};

    while (true) {
        const char = in_stream.readByte() catch break;

        if (!board.contains(pos)) ans += 1;

        try board.put(pos, true);

        switch (char) {
            '>' => pos.xright(),
            '<' => pos.xleft(),
            'v' => pos.ydown(),
            '^' => pos.yup(),
            '\n' => break,
            else => unreachable,
        }
    }

    std.debug.print("01: {}\n", .{ans});
}

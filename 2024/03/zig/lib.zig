const std = @import("std");

pub fn readFile(path: []const u8, allocator: std.mem.Allocator) !std.ArrayList(u8) {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    const reader = buf_reader.reader();

    var content = std.ArrayList(u8).init(allocator);

    const writter = content.writer();

    while (true) {
        const byte = reader.readByte() catch break;

        try writter.writeByte(byte);
    }

    return content;
}

test readFile {
    const file = try readFile("../input.txt", std.testing.allocator);
    defer file.deinit();

    try std.testing.expect(file.items.len == 19265);
}

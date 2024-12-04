const std = @import("std");

pub const TokenKind = enum {
    OpenParen,
    CloseParen,
    Comma,
    Number,
    Mul,
    Any,
};

pub const Token = struct {
    kind: TokenKind,
    value: []const u8,
};

pub const Tokens = std.ArrayList(Token);

pub const Tokenizer = struct {
    tokens: Tokens,

    const Self = @This();

    pub fn init(allocator: std.mem.Allocator) Tokenizer {
        return Tokenizer{
            .tokens = Tokens.init(allocator),
        };
    }

    pub fn deinit(self: *Self) void {
        self.tokens.deinit();
    }

    pub fn display(self: Self) void {
        std.debug.print("size: {d}\n", .{self.tokens.items.len});

        for (self.tokens.items) |token| {
            std.debug.print("{any} {s}\n", .{ token.kind, token.value });
        }
    }

    pub fn tokenize(self: *Self, text: []const u8) !Tokens {
        var cursor: usize = 0;
        const size = text.len;
        var bot: usize = 0;

        while (cursor < size - 1) : (cursor += 1) {
            bot = cursor;

            const char = text[cursor];

            const token: ?Token = switch (char) {
                '(' => Token{ .kind = .OpenParen, .value = text[bot .. cursor + 1] },
                ')' => Token{ .kind = .CloseParen, .value = text[bot .. cursor + 1] },
                ',' => Token{ .kind = .Comma, .value = text[bot .. cursor + 1] },
                'a'...'z' => text: {
                    matchString(size, &cursor, &text);

                    const string = text[bot .. cursor + 1];

                    if (std.mem.eql(u8, string, "mul")) {
                        break :text Token{ .kind = .Mul, .value = string };
                    }

                    break :text Token{ .kind = .Any, .value = string };
                },
                '0'...'9' => number: {
                    matchNumber(size, &cursor, &text);

                    break :number Token{ .kind = .Number, .value = text[bot .. cursor + 1] };
                },
                else => Token{ .kind = .Any, .value = text[bot .. cursor + 1] },
            };

            if (token != null) {
                try self.tokens.append(token.?);
            }
        }

        return self.tokens;
    }

    fn matchString(size: usize, cursor: *usize, text: *const []const u8) void {
        while (cursor.* < size - 1) : (cursor.* += 1) {
            switch (text.*[cursor.* + 1]) {
                'a'...'z' => {},
                else => break,
            }
        }
    }

    fn matchNumber(size: usize, cursor: *usize, text: *const []const u8) void {
        while (cursor.* < size - 1) : (cursor.* += 1) {
            switch (text.*[cursor.* + 1]) {
                '0'...'9' => {},
                else => break,
            }
        }
    }
};

test Tokenizer {
    var tokenizer = Tokenizer.init(std.testing.allocator);

    defer tokenizer.deinit();

    const text = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
    const tokens = try tokenizer.tokenize(text);

    tokenizer.display();

    try std.testing.expect(tokens.items.len == 34);
}

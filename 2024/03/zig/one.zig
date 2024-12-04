const std = @import("std");
const readFile = @import("./lib.zig").readFile;
const tk = @import("./tokenizer.zig");
const Parser = @import("./parser.zig").Parser;

const Tokenizer = tk.Tokenizer;
const Tokens = tk.Tokens;
const Token = tk.Token;
const TokenKind = tk.TokenKind;

pub fn one() !u32 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const content = try readFile("../input.txt", allocator);

    defer content.deinit();

    var tokenizer = Tokenizer.init(allocator);
    defer tokenizer.deinit();

    const tokens = try tokenizer.tokenize(content.items);

    var parser = Parser.init(allocator);

    defer parser.deinit();

    const expressions = try parser.parse(tokens);

    var sum: u32 = 0;

    for (expressions.items) |expression| {
        sum += expression.left * expression.right;
    }

    return sum;
}

test one {
    const answer = 187194524;

    const result = try one();

    std.debug.print("{d} {d}\n", .{ answer, result });
    try std.testing.expect(result == answer);
}

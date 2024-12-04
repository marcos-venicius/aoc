const std = @import("std");
const tk = @import("./tokenizer.zig");

const Tokenizer = tk.Tokenizer;
const Tokens = tk.Tokens;
const Token = tk.Token;
const TokenKind = tk.TokenKind;

const InvalidExpression = error{ InvalidNumber, UnexpectedToken, EndOfTokens };

const Expression = struct {
    left: u32 = 0,
    right: u32 = 0,
};

const Expressions = std.ArrayList(Expression);

pub const Parser = struct {
    expressions: Expressions,
    size: usize = 0,
    cursor: usize = 0,
    tokens: *const Tokens = undefined,

    const Self = @This();

    pub fn init(allocator: std.mem.Allocator) Parser {
        return Parser{
            .expressions = Expressions.init(allocator),
        };
    }

    pub fn deinit(self: *Self) void {
        self.expressions.deinit();
    }

    pub fn display(self: Self) void {
        for (self.expressions.items) |expression| {
            std.debug.print("{d} * {d}\n", .{ expression.left, expression.right });
        }
    }

    pub fn parse(self: *Self, tokens: Tokens) !Expressions {
        self.tokens = &tokens;
        self.size = tokens.items.len;

        while (self.cursor < self.size) {
            const expression: ?Expression = self.parseExpression() catch null;

            if (expression != null) {
                try self.expressions.append(expression.?);
            } else {
                self.cursor += 1;
            }
        }

        return self.expressions;
    }

    fn expect(self: *Self, kind: TokenKind) InvalidExpression!*Token {
        if (self.cursor >= self.size) return InvalidExpression.EndOfTokens;

        const next = &self.tokens.items[self.cursor];

        if (next.kind != kind) return InvalidExpression.UnexpectedToken;

        self.cursor += 1;

        return next;
    }

    fn parseExpression(self: *Self) InvalidExpression!Expression {
        _ = try self.expect(TokenKind.Mul);
        _ = try self.expect(TokenKind.OpenParen);
        const left = try self.expect(TokenKind.Number);
        _ = try self.expect(TokenKind.Comma);
        const right = try self.expect(TokenKind.Number);
        _ = try self.expect(TokenKind.CloseParen);

        const leftNumber = std.fmt.parseInt(u32, left.value, 10) catch return InvalidExpression.InvalidNumber;
        const rightNumber = std.fmt.parseInt(u32, right.value, 10) catch return InvalidExpression.InvalidNumber;

        return Expression{ .left = leftNumber, .right = rightNumber };
    }
};

test Parser {
    var tokenizer = Tokenizer.init(std.testing.allocator);

    defer tokenizer.deinit();

    const text = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
    const tokens = try tokenizer.tokenize(text);

    var parser = Parser.init(std.testing.allocator);

    defer parser.deinit();

    const expressions = try parser.parse(tokens);

    parser.display();

    try std.testing.expect(expressions.items.len == 4);
}

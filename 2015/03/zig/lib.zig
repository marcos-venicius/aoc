pub const Vector2 = struct {
    x: i32 = 0,
    y: i32 = 0,

    const Self = @This();

    pub fn xright(self: *Self) void {
        self.x += 1;
    }

    pub fn xleft(self: *Self) void {
        self.x -= 1;
    }

    pub fn yup(self: *Self) void {
        self.y -= 1;
    }

    pub fn ydown(self: *Self) void {
        self.y += 1;
    }
};

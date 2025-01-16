#define WITH_ANIMATION 1
#define WIDTH 1000
#define HEIGHT 800
#define BOX_SIZE 5

#include "./io.h"
#include "./aoc.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <raymath.h>

#if WITH_ANIMATION
#include <raylib.h>
#endif

typedef enum {
    N_SPACE = 0,
    N_WALL,
    N_END,
    N_START
} Node_Kind;

typedef struct {
    Node_Kind kind;
    VectorI2 pos;
} Node;

typedef struct {
    Node *nodes;
    size_t size;
    size_t w, h;
    VectorI2 end;
    VectorI2 start;
} Board;

int main(void) {
    char *content = NULL;

    const size_t size = read_file("./input.txt", &content);

    VectorI2 grid_size = get_grid_size(content, size);

    Board board = {
        .w = grid_size.x,
        .h = grid_size.y,
        .size = grid_size.x * grid_size.y,
        .nodes = NULL
    };

    board.nodes = malloc(board.size * sizeof(Node));

    CHECK_ALLOC(board.nodes);

    size_t ni = 0;

    ITER_OVER(content, char, size)
        VectorI2 pos = VPOS(ni, board.w);

        switch (it) {
        case '#': board.nodes[ni++] = (Node){ .pos = pos, .kind = N_WALL }; break;
        case '.': board.nodes[ni++] = (Node){ .pos = pos, .kind = N_SPACE }; break;
        case 'S': {
            board.nodes[ni++] = (Node){ .pos = pos, .kind = N_START };
            board.start = pos;
        } break;
        case 'E': {
            board.nodes[ni++] = (Node){ .pos = pos, .kind = N_END };
            board.end = pos;
        } break;
        case '\n': break;
        default: assert(0 && "invalid board item"); break;
        }
    ITER_END

    #if WITH_ANIMATION
    VectorI2 middle = {
        .x = WIDTH / 2 - board.w * BOX_SIZE / 2,
        .y = HEIGHT / 2 - board.h * BOX_SIZE / 2
    };

    InitWindow(WIDTH, HEIGHT, "AOC 16");

    Camera2D camera = {0};

    camera.target = (Vector2){middle.x, middle.y};
    camera.offset = (Vector2){middle.x, middle.y};
    camera.rotation = 0.f;
    camera.zoom = 1.f;

    Vector2 previousMousePosition = {0};
    bool dragging = false;

    while (!WindowShouldClose()) {
        PollInputEvents();

        BeginDrawing();

        BeginMode2D(camera);

        ClearBackground(BLACK);

        ITER_OVER(board.nodes, Node, board.size)
            switch (it.kind) {
            case N_SPACE: break;
            case N_WALL: DrawRectangle(it.pos.x * BOX_SIZE + middle.x, it.pos.y * BOX_SIZE + middle.y, BOX_SIZE, BOX_SIZE, RED); break;
            case N_START: DrawRectangle(it.pos.x * BOX_SIZE + middle.x, it.pos.y * BOX_SIZE + middle.y, BOX_SIZE, BOX_SIZE, WHITE); break;
            case N_END: DrawRectangle(it.pos.x * BOX_SIZE + middle.x, it.pos.y * BOX_SIZE + middle.y, BOX_SIZE, BOX_SIZE, GREEN); break;
            default: break;
            }
        ITER_END

        EndMode2D();

        EndDrawing();

        if (GetMouseWheelMove() > 0) camera.zoom += 0.1f;
        if (GetMouseWheelMove() < 0) camera.zoom -= 0.1f;

        if (camera.zoom < .5f) camera.zoom = .5f;
        if (camera.zoom > 3.f) camera.zoom = 3.f;

        if (IsMouseButtonDown(MOUSE_BUTTON_LEFT)) {
            Vector2 currentMousePosition = GetMousePosition();

            if (!dragging) {
                dragging = true;
            } else {
                Vector2 delta = Vector2Subtract(previousMousePosition, currentMousePosition);
                camera.target = Vector2Add(camera.target, Vector2Scale(delta, 1.f / camera.zoom));
            }

            previousMousePosition = currentMousePosition;
        } else {
            dragging = false;
        }
    }

    CloseWindow();
    #endif

    free(board.nodes);
    printfn("Part 01: 0");

    return 0;
}

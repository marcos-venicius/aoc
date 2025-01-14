#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <raylib.h>

#define FINAL
//#define WITH_ANIMATION

#define WIDTH 800
#define HEIGHT 800

typedef enum {
    M_TOP = '^',
    M_RIGHT = '>',
    M_BOTTOM = 'v',
    M_LEFT = '<'
} Movement;

typedef enum {
    BK_WALL,
    BK_BOX,
    BK_SPACE,
    BK_ROBOT
} Block_Kind;

typedef struct {
    Block_Kind kind;
    Vector2 pos;
    bool marked;
} Block;

typedef struct {
    size_t w, h;
    size_t size;
    Block *blocks;
    Block robot;
} Board;

static size_t next_movement_index = 0;
static size_t movements_count = 0;

#ifdef FINAL
#define BSIZE 10
static char *input_string = NULL;
static char *movements_string = NULL;
#else
#define BSIZE 20
static const char *input_string = "########\n"
                                  "#..O.O.#\n"
                                  "##@.O..#\n"
                                  "#...O..#\n"
                                  "#.#.O..#\n"
                                  "#...O..#\n"
                                  "#......#\n"
                                  "########\n";

static const char *movements_string = "<^^>>>vv<v>>v<<";
#endif


Vector2 get_input_size(void) {
    int w = 0;
    int h = 0;
    int last_br = 0;

    for (size_t i = 0; i < strlen(input_string); ++i) {
        if (input_string[i] == '\n') {
            if ((int)(i - last_br - 1) > w) w = i - last_br - 1;
            
            last_br = i;
            ++h;
        }
    }

    return (Vector2){
        .x = w,
        .y = h
    };
}

Board get_board(void) {
    Vector2 input_size = get_input_size();
    Board board = {
        .w = input_size.x,
        .h = input_size.y,
        .size = input_size.x * input_size.y,
    };

    board.blocks = malloc(board.size * sizeof(Block));

    if (board.blocks == NULL) {
        fprintf(stderr, "could not allocate enough memory for the blocks: %s\n", strerror(errno));
        exit(1);
    }

    size_t block_index = 0;
    int x = 0;
    int y = 0;

    for (size_t i = 0; i < strlen(input_string); ++i) {
        if (input_string[i] == '\n') {
            x = 0;
            ++y;
        } else {
            Block_Kind kind = BK_SPACE;

            switch (input_string[i]) {
                case '#': kind = BK_WALL; break;
                case '.': kind = BK_SPACE; break;
                case 'O': kind = BK_BOX; break;
                case '@': kind = BK_ROBOT; break;
                default: assert(0 && "invalid block kind");
            }

            board.blocks[block_index++] = (Block){
                .pos = { .x = x, .y = y },
                .kind = kind,
                .marked = false
            };

            if (kind == BK_ROBOT) board.robot = board.blocks[block_index - 1];

            ++x;
        }
    }
    
    return board;
}

Vector2 get_block_render_pos(const Block *block, Vector2 offset) {
    #ifdef FINAL
    float x = (block->pos.x * BSIZE) + offset.x;
    float y = (block->pos.y * BSIZE) + offset.y;
    #else
    float x = block->pos.x + (block->pos.x * BSIZE) + offset.x;
    float y = block->pos.y + (block->pos.y * BSIZE) + offset.y;
    #endif

    return (Vector2){
        .x = x,
        .y = y
    };
}

void render_board(const Board *board, Vector2 offset) {
    for (size_t i = 0; i < board->size; ++i) {
        Block block = board->blocks[i];

        Vector2 p = get_block_render_pos(&block, offset);

        switch (block.kind) {
            case BK_ROBOT:
                DrawRectangle(p.x, p.y, BSIZE, BSIZE, GREEN);
                break;
            case BK_BOX:
                DrawRectangle(p.x, p.y, BSIZE, BSIZE, block.marked ? YELLOW : WHITE);
                break;
            case BK_SPACE:
                DrawRectangle(p.x, p.y, BSIZE, BSIZE, GRAY);
                break;
            case BK_WALL:
                DrawRectangle(p.x, p.y, BSIZE, BSIZE, RED);
                break;
        }
    }
}

Movement *get_movements(void) {
    size_t size = strlen(movements_string);
    Movement *movements = malloc(size * sizeof(Movement));

    if (movements == NULL) {
        fprintf(stderr, "could not allocate enough memory for the movements: %s\n", strerror(errno));
        exit(1);
    }

    size_t idx = 0;

    for (size_t i = 0; i < size; ++i) {
        switch (movements_string[i]) {
            case '^': {
                movements[idx++] = M_TOP;
                ++movements_count;
            } break;
            case '>': {
                movements[idx++] = M_RIGHT;
                ++movements_count;
            } break;
            case 'v': {
                movements[idx++] = M_BOTTOM;
                ++movements_count;
            } break;
            case '<': {
                movements[idx++] = M_LEFT;
                ++movements_count;
            } break;
            case '\n': break;
            default: fprintf(stderr, "movement kind [%c] is not valid\n", movements_string[i]); exit(1);
        }
    }

    return movements;
}

void render_next_movement(const Movement *movements) {
    if (movements_count == next_movement_index) {
        int width = MeasureText("DONE", 50);

        DrawText("DONE", WIDTH / 2 - width / 2, HEIGHT - HEIGHT * 0.1, 50, WHITE);
    } else {
        Movement movement = movements[next_movement_index];

        char text[2] = {movement, '\0'};

        DrawText(text, WIDTH / 2, HEIGHT - HEIGHT * 0.1, 50, WHITE);
    }
}

Vector2 dec_y(Vector2 x) {
    return (Vector2){
        .x = x.x,
        .y = x.y - 1
    };
}

Vector2 inc_y(Vector2 x) {
    return (Vector2){
        .x = x.x,
        .y = x.y + 1
    };
}

Vector2 dec_x(Vector2 x) {
    return (Vector2){
        .x = x.x - 1,
        .y = x.y
    };
}

Vector2 inc_x(Vector2 x) {
    return (Vector2){
        .x = x.x + 1,
        .y = x.y
    };
}

int pos_to_index(const Board *board, Vector2 pos) {
    return (int)pos.y * board->w + (int)pos.x;
}

bool is_out_of_bounds(const Board *board, Vector2 p) {
    return p.x < 0 || p.x >= board->w || p.y < 0 || p.y >= board->h;
}

bool is_wall(const Board *board, int i) {
    return board->blocks[i].kind == BK_WALL;
}

bool is_box(const Board *board, int i) {
    return board->blocks[i].kind == BK_BOX;
}

void swap(Board *board, size_t robot, size_t b) {
    Block t = board->blocks[robot];

    board->blocks[robot] = board->blocks[b];
    board->blocks[b] = t;

    board->robot = board->blocks[b];
}

bool move_left(Board *board, Vector2 block) {
    int ri = pos_to_index(board, block);
    int i = pos_to_index(board, dec_x(block));

    if (is_out_of_bounds(board, dec_x(block))) return false;

    if (is_wall(board, ri) || is_wall(board, i)) return false;

    if (is_box(board, i) && !move_left(board, dec_x(block))) return false;

    board->blocks[ri].pos = dec_x(board->blocks[ri].pos);
    board->blocks[i].pos = inc_x(board->blocks[i].pos);

    swap(board, ri, i);

    board->robot = board->blocks[i];

    return true;
}

bool move_right(Board *board, Vector2 block) {
    size_t ri = pos_to_index(board, block);
    size_t i = pos_to_index(board, inc_x(block));

    if (is_out_of_bounds(board, inc_x(block))) return false;

    if (is_wall(board, ri) || is_wall(board, i)) return false;

    if (is_box(board, i) && !move_right(board, inc_x(block))) return false;

    board->blocks[ri].pos = inc_x(board->blocks[ri].pos);
    board->blocks[i].pos = dec_x(board->blocks[i].pos);

    swap(board, ri, i);
    
    return true;
}

bool move_top(Board *board, Vector2 block) {
    size_t ri = pos_to_index(board, block);
    size_t i = pos_to_index(board, dec_y(block));

    if (is_out_of_bounds(board, dec_y(block))) return false;

    if (is_wall(board, ri) || is_wall(board, i)) return false;

    if (is_box(board, i) && !move_top(board, dec_y(block))) return false;

    board->blocks[ri].pos = dec_y(board->blocks[ri].pos);
    board->blocks[i].pos = inc_y(board->blocks[i].pos);

    swap(board, ri, i);

    return true;
}

bool move_bottom(Board *board, Vector2 block) {
    size_t ri = pos_to_index(board, block);
    size_t i = pos_to_index(board, inc_y(block));

    if (is_out_of_bounds(board, inc_y(block))) return false;

    if (is_wall(board, ri) || is_wall(board, i)) return false;

    if (is_box(board, i) && !move_bottom(board, inc_y(block))) return false;

    board->blocks[ri].pos = inc_y(board->blocks[ri].pos);
    board->blocks[i].pos = dec_y(board->blocks[i].pos);

    swap(board, ri, i);

    return true;
}

void execute_movement(Board *board, Movement movement) {
    switch (movement) {
        case M_TOP: move_top(board, board->robot.pos); break;
        case M_RIGHT: move_right(board, board->robot.pos); break;
        case M_BOTTOM: move_bottom(board, board->robot.pos); break;
        case M_LEFT: move_left(board, board->robot.pos); break;
        default: fprintf(stderr, "movement kind [%c] is not valid\n", movement); exit(1);
    }
}

char *read_file(const char *filename) {
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        fprintf(stderr, "could not open input file %s due to %s\n", filename, strerror(errno));
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    const size_t size = ftell(file);
    rewind(file);

    char *content = malloc(size * sizeof(char));

    if (content == NULL) {
        fprintf(stderr, "could not allocate emory enough: %s\n", strerror(errno));
        return NULL;
    }

    const size_t read_size = fread(content, 1, size, file);

    if (read_size != size) {
        fprintf(stderr, "could not read file %s due to: %s\n", filename, strerror(errno));
        free(content);
        fclose(file);
        return NULL;
    }

    fclose(file);

    return content;
}

bool load_inputs_from_files(void) {
    input_string = read_file("./input-01.txt");

    if (input_string == NULL) return false;

    movements_string = read_file("./input-02.txt");

    if (movements_string == NULL) return false;

    return true;
}

#ifdef WITH_ANIMATION
int main(void) {
    #ifdef FINAL
    if (!load_inputs_from_files()) exit(1);
    #endif

    InitWindow(WIDTH, HEIGHT, "AOC 15");

    Board board = get_board();
    Movement *movements = get_movements();

    fprintf(stderr, "%ld\n", movements_count);

    SetTargetFPS(400);

    Vector2 middle = {
        .x = WIDTH / 2.f - (board.w * BSIZE) / 2.f,
        .y = HEIGHT / 2.f - (board.h * BSIZE) / 2.f
    };

    bool get_sum = false;

    while (!WindowShouldClose()) {
        PollInputEvents();

        BeginDrawing();

        ClearBackground(BLACK);

        render_board(&board, middle);

        #ifndef FINAL
        render_next_movement(movements);
        #endif

        EndDrawing();

        #ifdef FINAL
        if (next_movement_index < movements_count) {
            execute_movement(&board, movements[next_movement_index++]);
        } else {
            get_sum = true;
            break;
        }
        #else
        if (IsKeyPressed(KEY_ENTER)) {
            if (next_movement_index < movements_count) {
                execute_movement(&board, movements[next_movement_index++]);
            } else {
                get_sum = true;
                break;
            }
        }
        #endif
    }

    #ifdef FINAL
    SetTargetFPS(120);
    #else
    SetTargetFPS(5);
    #endif

    size_t block = 0;
    size_t sum = 0;
    bool show_result = false;

    while (!WindowShouldClose() && get_sum) {
        BeginDrawing();

        ClearBackground(BLACK);

        render_board(&board, middle);

        if (block < board.size) {
            Block b = board.blocks[block];

            if (b.kind == BK_BOX) {
                sum += 100 * b.pos.y + b.pos.x;

                board.blocks[block].marked = true;
            }

            ++block;
        } else {
            show_result = true;
            break;
        }

        EndDrawing();
    }

    char result[20];

    sprintf(result, "%ld", sum);

    int w = MeasureText(result, 50);

    while (!WindowShouldClose() && show_result) {
        BeginDrawing();

        ClearBackground(BLACK);

        DrawText(result, WIDTH / 2 - w / 2, HEIGHT / 2 - 25, 50, WHITE);

        EndDrawing();
    }

    free(board.blocks);
    free(movements);

    #ifdef FINAL
    free(input_string);
    free(movements_string);
    #endif
    CloseWindow();

    return 0;
}
#else
int main(void) {
    #ifdef FINAL
    if (!load_inputs_from_files()) exit(1);
    #endif

    Board board = get_board();
    Movement *movements = get_movements();


    while (next_movement_index < movements_count) execute_movement(&board, movements[next_movement_index++]);

    size_t sum = 0;

    for (size_t block = 0; block < board.size; ++block) {
        Block b = board.blocks[block];

        if (b.kind == BK_BOX) {
            sum += 100 * b.pos.y + b.pos.x;

            board.blocks[block].marked = true;
        }
    }

    printf("Part 01: %ld\n", sum);

    free(board.blocks);
    free(movements);

    #ifdef FINAL
    free(input_string);
    free(movements_string);
    #endif

    return 0;
}
#endif

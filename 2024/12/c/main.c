#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "map.h"
#include "ll.h"

#define LEN(arr) sizeof(arr) / sizeof(arr[0])

typedef struct {
    int x, y;
} Vec2;

typedef struct {
    char **grid;
    Map* cache;
    int size;
} Grid;

int grid_size(const char *filepath) {
    FILE* file = fopen(filepath, "rb");

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);

    int row_size = 0;

    while (row_size < file_size) {
        row_size++;

        char bytes[1];

        size_t size = fread(bytes, 1, 1, file);

        if (bytes[0] == '\n' || size == 0) {
            break;
        }
    }

    fclose(file);

    return file_size / row_size;
}


Grid grid_load(const char *filepath) {
    Grid grid = {0};

    grid.cache = map_new();

    grid.size = grid_size(filepath);

    grid.grid = calloc(grid.size, sizeof(char*));

    for (int i = 0; i < grid.size; i++) {
        grid.grid[i] = calloc(grid.size, sizeof(char));
    }

    FILE* file = fopen(filepath, "rb");

    for (int y = 0; y < grid.size; y++) {
        for (int x = 0; x < grid.size; x++) {
            char bytes[1];

            size_t size = fread(bytes, 1, 1, file);

            if (bytes[0] == '\n' || size == 0) {
                size = fread(bytes, 1, 1, file);
            }

            grid.grid[y][x] = bytes[0];
        }
    }

    fclose(file);

    return grid;
}

int get_area(Grid *grid, LL *ll, char of, int x, int y) {
    if (map_get(grid->cache, x, y) != NULL) {
        return 0;
    }

    if (grid->grid[y][x] != of) {
        return 0;
    }

    ll_add(ll, &(Vec2){.x = x, .y = y}, sizeof(Vec2));

    map_set(grid->cache, x, y, 0);

    int result = 1;

    if (x - 1 >= 0) {
        result += get_area(grid, ll, of, x - 1, y);
    }

    if (x + 1 < grid->size) {
        result += get_area(grid, ll, of, x + 1, y);
    }

    if (y - 1 >= 0) {
        result += get_area(grid, ll, of, x, y - 1);
    }

    if (y + 1 < grid->size) {
        result += get_area(grid, ll, of, x, y + 1);
    }

    return result;
}

bool is_out_of_bounds(Grid *grid, Vec2 vec) {
    return vec.x < 0 || vec.y < 0 || vec.x >= grid->size || vec.y >= grid->size;
}

int get_perimeter(Grid *grid, LL *ll) {
    int perimeter = 0;

    Vec2 directions[] = {
        {.x = 1, .y = 0},
        {.x = -1, .y = 0},
        {.x = 0, .y = 1},
        {.x = 0, .y = -1},
    };

    LLNode *current = ll->root;

    while (current != NULL) {
        Vec2 *data = (Vec2*)current->data;

        for (int i = 0; i < 4; i++) {
            Vec2 dir = directions[i];
            Vec2 pos = {
                .x = data->x + dir.x,
                .y = data->y + dir.y,
            };

            if (is_out_of_bounds(grid, pos) || grid->grid[pos.y][pos.x] != grid->grid[data->y][data->x]) {
                perimeter++;
            }
        }

        current = current->next;
    }

    return perimeter;
}

void grid_free(Grid *grid) {
    for (int i = 0; i < grid->size; i++) {
        free(grid->grid[i]);
    }

    map_free(grid->cache);
    free(grid->grid);
}

void usage(FILE *stream, const char* program_name) {
    fprintf(stream, "Usage: %s FILE\n", program_name);
    fprintf(stream, "Execute day one and two of the current challenge given the input file\n");
    fprintf(stream, "\n");
    fprintf(stream, "    --help -h        show this help message\n");
    fprintf(stream, "\n");
    fprintf(stream, "Advent Of Code 2024 day 12 - https://github.com/marcos-venicius/aoc/tree/main/2024/12/c\n");
}

int main(int argc, char **argv) {
    if (argc != 2) {
        usage(stderr, argv[0]);

        exit(1);
    }

    if (strncmp(argv[1], "-h", 2) == 0 || strncmp(argv[1], "--help", 6) == 0) {
        usage(stdout, argv[0]);

        exit(0);
    }

    Grid grid = grid_load(argv[1]);

    int result = 0;

    for (int y = 0; y < grid.size; y++) {
        for (int x = 0; x < grid.size; x++) {
            if (map_get(grid.cache, x, y) != NULL) continue;

            LL *ll = ll_new();

            int area = get_area(&grid, ll, grid.grid[y][x], x, y);
            int perimeter = get_perimeter(&grid, ll);

            ll_free(ll);

            result += area * perimeter;
            /* printf("A region of %c plants with price %d * %d\n", grid.grid[y][x], area, perimeter); */
        }
    }

    printf("Part 01: %d\n", result);

    grid_free(&grid);

    return 0;
}

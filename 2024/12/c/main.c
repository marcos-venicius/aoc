#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "map.h"

#define LEN(arr) sizeof(arr) / sizeof(arr[0])

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

int get_area(Grid *grid, char of, int x, int y) {
    if (map_get(grid->cache, x, y) != NULL) {
        return 0;
    }

    if (grid->grid[y][x] != of) {
        return 0;
    }

    map_set(grid->cache, x, y, 0);

    int result = 1;

    if (x - 1 >= 0) {
        result += get_area(grid, of, x - 1, y);
    }

    if (x + 1 < grid->size) {
        result += get_area(grid, of, x + 1, y);
    }

    if (y - 1 >= 0) {
        result += get_area(grid, of, x, y - 1);
    }

    if (y + 1 < grid->size) {
        result += get_area(grid, of, x, y + 1);
    }

    return result;
}

void grid_free(Grid *grid) {
    for (int i = 0; i < grid->size; i++) {
        free(grid->grid[i]);
    }

    map_free(grid->cache);
    free(grid->grid);
}

int main() {
    Grid grid = grid_load("../test.txt");

    for (int y = 0; y < grid.size; y++) {
        for (int x = 0; x < grid.size; x++) {
            if (map_get(grid.cache, x, y) != NULL) continue;

            int area = get_area(&grid, grid.grid[y][x], x, y);

            printf("Area of %c: %d\n", grid.grid[y][x], area);
        }
    }

    grid_free(&grid);

    return 0;
}

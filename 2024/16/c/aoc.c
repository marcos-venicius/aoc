#include "./aoc.h"
#include <stdio.h>

int printfn(const char *format, ...) {
    va_list args;
    va_start(args, format);
    int result = vprintf(format, args);
    printf("\n");
    va_end(args);

    return result;
}

VectorI2 get_grid_size(const char *input, size_t input_size) {
    size_t w = 0;
    size_t h = 0;
    size_t c = 0;

    for (size_t i = 0; i < input_size; ++i) {
        char chr = input[i];

        if (chr == '\n') {
            if (c > w) w = c;

            ++h;
            c = 0;
        } else {
            ++c;
        }
    }

    return (VectorI2){
        .x = w,
        .y = h
    };
}

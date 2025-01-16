#define WITH_ANIMATION 1

#include <stdio.h>
#include "./io.h"

#if WITH_ANIMATION
#include <raylib.h>
#endif

int main(void) {
    const size_t size = read_file("./input.txt", NULL);

    printf("Part 01: %ld\n", size);

    return 0;
}

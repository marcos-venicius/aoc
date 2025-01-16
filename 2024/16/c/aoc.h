#ifndef AOC_H_
#define AOC_H_

#include <raylib.h>
#include <stddef.h>
#include <errno.h>
#include <string.h>

#define CHECK_ALLOC(ptr) if (ptr == NULL) fprintf(stderr, "could not allocate memory enough for \""#ptr"\" due to: %s\n", strerror(errno))

#define ITER_OVER(array, type, size) { for (size_t i = 0; i < (size); ++i) { type it = (array)[i];
#define ITER_END }}

#define IPOS(x, y, w) (x) + (y) * (w)
#define VPOS(i, w) (VectorI2){ .x = (i) % (w), .y = (i) / (w) }

typedef struct {
    size_t x, y;
} VectorI2;

VectorI2 get_grid_size(const char *input, size_t input_size);
int printfn(const char *format, ...);

#endif // AOC_H_

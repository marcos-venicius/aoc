#include "./io.h"
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>

size_t read_file(const char *filename, char **content_out) {
    FILE *fptr = fopen(filename, "r");

    if (fptr == NULL) {
        fprintf(stderr, "could not open file '%s' due to: %s\n", filename, strerror(errno));
        exit(1);
    }

    fseek(fptr, 0, SEEK_END);
    const size_t size = ftell(fptr);
    rewind(fptr);

    if (content_out == NULL) {
        fclose(fptr);

        return size;
    }

    *content_out = malloc((size + 1) * sizeof(char));

    if (*content_out == NULL) {
        fprintf(stderr, "could not allocate memory enough for file '%s' of size %ld due to: %s\n", filename, size, strerror(errno));
        exit(1);
    }

    const size_t read_size = fread(*content_out, 1, size, fptr);
    
    if (read_size != size) {
        free(*content_out);
        fclose(fptr);
        fprintf(stderr, "could not read whole file '%s' of size %ld, only read %ld due to: %s", filename, size, read_size, strerror(errno));
        exit(1);
    }

    (*content_out)[size] = '\0';

    fclose(fptr);

    return size;
}

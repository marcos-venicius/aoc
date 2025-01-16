#ifndef IO_H_
#define IO_H_

#include <stddef.h>

// read a file and return content via a pointer `content_out` and return the size of the file.
// if you don't provide a content out, only the size is returned without any allocation of memory.
size_t read_file(const char *filename, char **content_out);

#endif // IO_H_

#ifndef MAP_H_
#define MAP_H_

#include <stdint.h>
#include <stddef.h>

typedef struct Node Node;

struct Node {
    int64_t value;
    int64_t key;

    Node *next;
};

typedef struct {
    size_t capacity;
    Node *nodes[];
} Map;

Map *map_new(size_t capacity);
void map_set(Map *map, int64_t key, int64_t value);
Node *map_get(Map *map, int64_t key);
void map_free(Map *map);

#endif // MAP_H_

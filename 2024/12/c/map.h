#ifndef MAP_H_
#define MAP_H_

#include <stdint.h>
#include <stddef.h>

#define MAP_BUCKET_SIZE 1000

typedef unsigned long long int64;
typedef struct Node Node;

struct Node {
    int64 value;
    int64 n;
    int i;

    Node *next;
};

typedef struct {
    Node* nodes[MAP_BUCKET_SIZE];
    size_t size;
} Map;

Map *map_new();
void map_set(Map *map, int64 n, int i, int64 value);
Node *map_get(Map *map, int64 n, int i);
void map_free(Map *map);

#endif // MAP_H_

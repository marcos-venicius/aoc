#ifndef AOC_MAP_H_
#define AOC_MAP_H_

#include <stdint.h>
#include <stddef.h>

#define MAP_BUCKET_SIZE 1000

typedef struct MapNode MapNode;

struct MapNode {
    void *data;
    size_t data_size;

    // TODO: is possible to accept "dynamic" keys?
    char *key;

    MapNode *next;
};

typedef struct {
    MapNode* nodes[MAP_BUCKET_SIZE];
    size_t length;
} Map;

Map *map_new();
void map_set(Map *map, char *key, void *data, size_t data_size);
void map_set_i(Map *map, char *key, int value);
void map_set_string(Map *map, char *key, char *string);
void *map_get(Map *map, char *key);
void map_free(Map *map);

#endif // AOC_MAP_H_

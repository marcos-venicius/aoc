#include "map.h"
#include <stdlib.h>

Node *new_node(int64_t key, int64_t value) {
    Node *node = calloc(1, sizeof(Node));

    node->key = key;
    node->value = value;
    node->next = NULL;

    return node;
}

Map *map_new(size_t capacity) {
    Map *map = calloc(1, sizeof(Map) + sizeof(Node*) * capacity);

    map->capacity = capacity;

    return map;
}

void map_set(Map *map, int64_t key, int64_t value) {
    size_t index = key % map->capacity;

    Node *current = map->nodes[index];

    if (current == NULL) {
        map->nodes[index] = new_node(key, value);
    } else if (current->key == key) {
        current->value = value;
    } else {
        while (current->next != NULL && current->next->key != key) {
            current = current->next;
        }

        if (current->next == NULL) {
            current->next = new_node(key, value);
        } else {
            current->next->value = value;
        }
    }
}

Node *map_get(Map *map, int64_t key) {
    size_t index = key % map->capacity;

    Node *current = map->nodes[index];

    while (current != NULL && current->key != key) {
        current = current->next;
    }

    return current;
}

void map_free(Map *map) {
    for (size_t i = 0; i < map->capacity; i++) {
        Node *current = map->nodes[i];

        if (current != NULL) {
            while (current != NULL) {
                Node *next = current->next;

                free(current);

                current = next;
            }
        }
    }

    free(map);
}

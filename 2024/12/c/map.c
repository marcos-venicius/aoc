#include "map.h"
#include <string.h>
#include <stdlib.h>

int64 hash(int64 n, int i) {
    int64 hash = 5381;

    hash = ((hash << 5) + hash) + n;
    hash = ((hash << 5) + hash) + i;

    return hash % MAP_BUCKET_SIZE;
}

Node *new_node(Map* map, int64 n, int i, void *data, size_t data_size) {
    Node *node = calloc(1, sizeof(Node));

    node->i = i;
    node->n = n;
    node->next = NULL;

    if (data != NULL) {
        node->data = malloc(data_size);

        memcpy(node->data, data, data_size);
    }

    map->size++;

    return node;
}

Map *map_new() {
    return calloc(1, sizeof(Map));
}

void map_set(Map *map, int64 n, int i, void *data, size_t data_size) {
    size_t index = hash(n, i);

    Node *current = map->nodes[index];

    if (current == NULL) {
        map->nodes[index] = new_node(map, n, i, data, data_size);
    } else if (current->n == n && current->i == i) {
        memcpy(current->data, data, data_size);
    } else {
        while (current->next != NULL && (current->next->n != n || current->next->i != i)) {
            current = current->next;
        }

        if (current->next == NULL) {
            current->next = new_node(map, n, i, data, data_size);
        } else {
            memcpy(current->data, data, data_size);
        }
    }
}

Node *map_get(Map *map, int64 n, int i) {
    size_t index = hash(n, i);

    Node *current = map->nodes[index];

    while (current != NULL && (current->n != n || current->i != i)) {
        current = current->next;
    }

    return current;
}

void map_free(Map *map) {
    for (size_t i = 0; i < MAP_BUCKET_SIZE; i++) {
        Node *current = map->nodes[i];

        if (current != NULL) {
            while (current != NULL) {
                Node *next = current->next;

                free(current->data);
                free(current);

                current = next;
            }
        }
    }

    free(map);
}

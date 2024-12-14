#include "map.h"
#include <stdlib.h>

int64 hash(int64 n, int i) {
    int64 hash = 5381;

    hash = ((hash << 5) + hash) + n;
    hash = ((hash << 5) + hash) + i;

    return hash % MAP_BUCKET_SIZE;
}

Node *new_node(int64 n, int i, int64 value) {
    Node *node = calloc(1, sizeof(Node));

    node->i = i;
    node->n = n;
    node->value = value;

    node->next = NULL;

    return node;
}

Map *map_new(size_t capacity) {
    return calloc(1, sizeof(Map));
}

void map_set(Map *map, int64 n, int i, int64 value) {
    size_t index = hash(n, i);

    Node *current = (*map)[index];

    if (current == NULL) {
        (*map)[index] = new_node(n, i, value);
    } else if (current->n == n && current->i == i) {
        current->value = value;
    } else {
        while (current->next != NULL && (current->next->n != n || current->next->i != i)) {
            current = current->next;
        }

        if (current->next == NULL) {
            current->next = new_node(n, i, value);
        } else {
            current->next->value = value;
        }
    }
}

Node *map_get(Map *map, int64 n, int i) {
    size_t index = hash(n, i);

    Node *current = (*map)[index];

    while (current != NULL && (current->n != n || current->i != i)) {
        current = current->next;
    }

    return current;
}

void map_free(Map *map) {
    for (size_t i = 0; i < MAP_BUCKET_SIZE; i++) {
        Node *current = (*map)[i];

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

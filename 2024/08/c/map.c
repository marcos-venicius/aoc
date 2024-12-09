#include <stdio.h>
#include <stdlib.h>
#include "map.h"

AntennaeMap* new_map() {
    return calloc(1, sizeof(AntennaeMap));
}

int get_index(char key) {
    if (key >= '0' && key <= '9') {
        return key - '0';
    }

    if (key >= 'a' && key <= 'z') {
        return (key - 'a') + 10;
    }

    if (key >= 'A' && key <= 'Z') {
        return (key - 'A') + 26 + 10;
    }

    return -1;
}

Antenna* get(AntennaeMap *map, char key) {
    int index = get_index(key);

    if (index < 0 || index >= ANTENNAE_MAP_SIZE) {
        printf("invalid index %d key: %c\n", index, key);
        exit(1);
    }

    if (map->antennae[index] != NULL) {
        return map->antennae[index];
    }

    return NULL;
}

void set(AntennaeMap *map, char key, Vector2 value) {
    int index = get_index(key);

    if (index < 0 || index >= ANTENNAE_MAP_SIZE) {
        printf("invalid index %d key: %c\n", index, key);
        exit(1);
    }
    
    Antenna* antenna = malloc(sizeof(Antenna));

    antenna->value = value;
    antenna->next = NULL;

    Antenna* current = map->antennae[index];

    if (current != NULL) {
        while (current->next != NULL) {
            current = current->next;
        }

        current->next = antenna;
    } else {
        map->antennae[index] = antenna;
    }
}

void free_map(AntennaeMap* map) {
    for (int i = 0; i < ANTENNAE_MAP_SIZE; i++) {
        Antenna* current = map->antennae[i];

        while (current != NULL) {
            Antenna* next = current->next;

            free(current);

            current = next;
        }
    }

    free(map);
}

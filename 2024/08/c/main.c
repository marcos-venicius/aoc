#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "types.h"
#include "set.c"

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

int max(int a, int b) {
    if (b > a) {
        return b;
    }

    return a;
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

    if (map->antennae[index] != NULL) {
        Antenna* current = map->antennae[index];

        while (current->next != NULL) {
            current = current->next;
        }

        current->next = antenna;
    } else {
        map->antennae[index] = antenna;
    }
}

AntennaeMap* load_map(char* mapfilepath) {
    AntennaeMap* map = malloc(sizeof(AntennaeMap));

    FILE* file = fopen(mapfilepath, "r");

    int y = 0, x = 0, w = 0, h = 0;

    char chr;

    while ((chr = fgetc(file)) != EOF) {
        switch (chr) {
            case '\n': {
                y++;
                x = 0;
                break;
            }
            case '.': {
                x++;
                break;
            }
            default: {
                Vector2 pos = { .x = x, .y = y };

                set(map, chr, pos);

                x++;
                break;
            }
        }

        w = max(x, w);
        h = max(y, h);
    }

    w = max(x, w);
    h = max(y, h);

    map->width = w;
    map->height = h;

    return map;
}

bool is_out_of_bounds(AntennaeMap* map, Vector2 vec) {
    return vec.x < 0 || vec.x >= map->width || vec.y < 0 || vec.y >= map->height;
}

void free_map(AntennaeMap* map) {
    for (int i = 0; i < ANTENNAE_MAP_SIZE; i++) {
        if (map->antennae[i] != NULL) {
            Antenna* current = map->antennae[i];

            while (current->next != NULL) {
                Antenna* next = current->next;

                free(current);

                current = next;
            }

            free(current);
        }
    }
}

void main() {
    AntennaeMap* map = load_map("../input.txt");
    Set* set = new_set(map->width * map->height);

    for (int i = 0; i < ANTENNAE_MAP_SIZE; i++) {
        if (map->antennae[i] != NULL) {
            Antenna* antenna_a = map->antennae[i];

            while (antenna_a != NULL) {
                Antenna* antenna_b = antenna_a->next;

                while (antenna_b != NULL) {
                    Vector2 ant1 = { .x = 2*antenna_a->value.x - antenna_b->value.x, .y = 2 * antenna_a->value.y - antenna_b->value.y };
                    Vector2 ant2 = { .x = 2*antenna_b->value.x - antenna_a->value.x, .y = 2 * antenna_b->value.y - antenna_a->value.y };

                    if (!is_out_of_bounds(map, ant1)) {
                        add_to_set(set, ant1);
                    }

                    if (!is_out_of_bounds(map, ant2)) {
                        add_to_set(set, ant2);
                    }

                    antenna_b = antenna_b->next;
                }

                antenna_a = antenna_a->next;
            }
        }
    }

    printf("01: %d\n", set->length);

    free_set(set);
    free_map(map);
}

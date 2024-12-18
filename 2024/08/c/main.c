#include <stdio.h>
#include <stdbool.h>
#include "types.h"
#include "set.h"
#include "map.h"

bool equals(Vector2 a, Vector2 b) {
    return a.x == b.x && a.y == b.y;
}

int max(int a, int b) {
    if (b > a) {
        return b;
    }

    return a;
}

AntennaeMap* load_map(char* mapfilepath) {
    AntennaeMap* map = new_map();

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

int one(AntennaeMap *map) {
    Set* set = new_set(map->width * map->height);

    for (int i = 0; i < ANTENNAE_MAP_SIZE; i++) {
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

    int ans = set->length;

    free_set(set);

    return ans;
}

int two(AntennaeMap *map) {
    Set* set = new_set(map->width * map->height);

    for (int i = 0; i < ANTENNAE_MAP_SIZE; i++) {
        Antenna* antenna_a = map->antennae[i];

        while (antenna_a != NULL) {
            Antenna* antenna_b = map->antennae[i];

            while (antenna_b != NULL) {
                if (!equals(antenna_a->value, antenna_b->value)) {
                    int dx = antenna_b->value.x - antenna_a->value.x;
                    int dy = antenna_b->value.y - antenna_a->value.y;

                    Vector2 antinode = { .x = antenna_a->value.x, .y = antenna_a->value.y };

                    while (!is_out_of_bounds(map, antinode)) {
                        add_to_set(set, antinode);

                        antinode.x -= dx;
                        antinode.y -= dy;
                    }
                }

                antenna_b = antenna_b->next;
            }

            antenna_a = antenna_a->next;
        }
    }

    int ans = set->length;

    free_set(set);

    return ans;
}

int main() {
    AntennaeMap* map = load_map("../input.txt");

    int one_ans = one(map);

    printf("01: %d\n", one_ans);

    int two_ans = two(map);

    printf("02: %d\n", two_ans);

    free_map(map);

    return 0;
}

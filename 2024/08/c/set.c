#include "set.h"
#include <stdlib.h>

Set* new_set(int capacity) {
    Set* set = malloc(sizeof(Set) + sizeof(Vector2) * capacity);

    set->capacity = capacity;
    set->length = 0;

    return set;
}

int add_to_set(Set* set, Vector2 value) {
    for (int i = 0; i < set->length; i++) {
        Vector2 item = set->items[i];

        if (item.x == value.x && item.y == value.y) {
            return 0;
        }
    }
    
    if (set->length == set->capacity) {
        return -1;
    }

    set->items[set->length] = value;
    set->length++;

    return 0;
}

void free_set(Set* set) {
    free(set);
}

#ifndef SET_H_
#define SET_H_

#include "types.h"

typedef struct {
    int length, capacity;
    Vector2 items[];
} Set;

Set* new_set(int capacity);
int add_to_set(Set* set, Vector2 value);
void free_set(Set* set);

#endif // SET_H_

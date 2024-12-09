#ifndef MAP_H_
#define MAP_H_

#include "types.h"

typedef struct Antenna Antenna;

struct Antenna {
    Vector2 value;
    Antenna* next;
};

typedef struct {
    Antenna* antennae[ANTENNAE_MAP_SIZE];
    int width, height;
} AntennaeMap;

AntennaeMap* new_map();
Antenna* get(AntennaeMap *map, char key);
void set(AntennaeMap *map, char key, Vector2 value);
void free_map(AntennaeMap* map);

#endif // MAP_H_

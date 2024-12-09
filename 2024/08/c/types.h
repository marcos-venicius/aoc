#ifndef TYPES_H_
#define TYPES_H_

#define ANTENNAE_MAP_SIZE 62

typedef struct {
    int x, y;
} Vector2;

typedef struct Antenna Antenna;

struct Antenna {
    Vector2 value;
    Antenna* next;
};

typedef struct {
    Antenna* antennae[ANTENNAE_MAP_SIZE];
    int width, height;
} AntennaeMap;

typedef struct {
    int length, capacity;
    Vector2 items[];
} Set;

#endif // TYPES_H_

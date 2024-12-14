#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "map.h"

#define LEN(arr) sizeof(arr) / sizeof(arr[0])

int64_t hash(int64_t a, int b) {
    int64_t hashcode = 23;
    hashcode = (hashcode * 37) + a;
    hashcode = (hashcode * 37) + b;

    return hashcode;
}

int int_to_string(int64_t n, char **out) {
    int length = snprintf(NULL, 0, "%ld", n);

    *out = malloc(length + 1);

    snprintf(*out, length + 1, "%ld", n);

    return length;
}

void split_string(char *str, int size, char **out_left, char **out_right) {
    int m = size / 2;

    *out_left = malloc(m + 1);
    *out_right = malloc(m + 1);

    for (int i = 0; i < m; i++) {
        (*out_left)[i] = str[i];
        (*out_right)[i] = str[m + i];
    }

    (*out_left)[m] = '\0';
    (*out_right)[m] = '\0';
}

int64_t solve(Map *map, int64_t n, int iterations) {
    if (iterations == 0) return 1;

    Node *cache = map_get(map, hash(n, iterations));

    if (cache != NULL) return cache->value;

    int64_t result = 0;

    if (n == 0) {
        result = solve(map, 1, iterations - 1);
        map_set(map, hash(n, iterations), result);

        return result;
    }

    char *str;

    int size = int_to_string(n, &str);

    if (size % 2 == 0) {
        char *left;
        char *right;

        split_string(str, size, &left, &right);

        int64_t leftN = strtoll(left, NULL, 10);
        int64_t rightN = strtoll(right, NULL, 10);

        result += solve(map, leftN, iterations - 1);
        result += solve(map, rightN, iterations - 1);

        map_set(map, hash(n, iterations), result);

        free(left);
        free(right);
        free(str);

        return result;
    }

    free(str);

    result = solve(map, n * 2024, iterations - 1);
    map_set(map, hash(n, iterations), result);

    return result;
}

int main() {
    int input[] = {77, 515, 6779622, 6, 91370, 959685, 0, 9861};
    int64_t part1 = 0;

    Map *map = map_new(75);

    for (size_t i = 0; i < LEN(input); i++) {
        part1 += solve(map, input[i], 25);
    }

    printf("Part 01: %ld\n", part1);

    map_free(map);

    return 0;
}

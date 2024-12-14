#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "map.h"

#define LEN(arr) sizeof(arr) / sizeof(arr[0])

static const int input[] = {77, 515, 6779622, 6, 91370, 959685, 0, 9861};
static const size_t input_size = LEN(input);

typedef unsigned long long int64;

int int_to_string(int64 n, char **out) {
    int length = snprintf(NULL, 0, "%lld", n);

    *out = malloc(length + 1);

    snprintf(*out, length + 1, "%lld", n);

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

int64 solve(Map *map, int64 n, int i) {
    if (i == 0) return 1;

    Node *cache = map_get(map, n, i);

    if (cache != NULL) return cache->value;

    int64 result;

    if (n == 0) {
        result = solve(map, 1, i - 1);

        map_set(map, n, i, result);

        return result;
    }

    char *str;

    int size = int_to_string(n, &str);

    if (size % 2 == 0) {
        char *left;
        char *right;

        split_string(str, size, &left, &right);

        int64 leftN = strtoll(left, NULL, 10);
        int64 rightN = strtoll(right, NULL, 10);

        result = solve(map, leftN, i - 1) + solve(map, rightN, i - 1);

        map_set(map, n, i, result);

        free(left);
        free(right);
        free(str);

        return result;
    }

    free(str);

    result = solve(map, n * 2024, i - 1);

    map_set(map, n, i, result);

    return result;
}

void one(Map *map) {
    int64 res = 0;

    for (size_t i = 0; i < input_size; i++) {
        res += solve(map, input[i], 25);
    }

    printf("Part 01: %lld\n", res);
}

void two(Map *map) {
    int64 res = 0;

    for (size_t i = 0; i < input_size; i++) {
        res += solve(map, input[i], 75);
    }

    printf("Part 02: %lld\n", res);
}

int main() {
    Map *map = map_new();

    one(map);
    two(map);

    map_free(map);

    return 0;
}

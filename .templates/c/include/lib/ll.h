#ifndef AOC_LL_H_
#define AOC_LL_H_
#include <stddef.h>
#include <stdbool.h>

typedef bool (*CompareCallback)(void *a, void *b);
typedef void (*FreeCallback)(void *);

typedef struct LLNode LLNode;

struct LLNode {
    void *data;
    LLNode *next;
};

typedef struct {
    LLNode *head;
    LLNode *tail;

    size_t count;

    // callbacks
    CompareCallback compare_callback;
    FreeCallback free_callback;
} LL;

LL *ll_new(FreeCallback free_callback, CompareCallback compare_callback);

// If the data size is 0, instead of allocating memory to the data
// we just pointer to it
void ll_add(LL *ll, void *data, size_t data_size);
void ll_add_i(LL *ll, int i);
void ll_add_s(LL *ll, char *s);

void ll_insert(LL *ll, size_t index, void *data);

void ll_remove_by_value(LL *ll, void *data);
void ll_remove_by_index(LL *ll, size_t index);

void *ll_find_by_value(LL *ll, void *data);
void *ll_find_by_index(LL *ll, size_t index);

void ll_free(LL *ll);

#endif // AOC_LL_H_

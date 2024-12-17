#ifndef AOC_LL_H_
#define AOC_LL_H_
#include <stddef.h>

// This macro is usefull when you want, for example, remove an integer and you don't want to create
// an extra variable to pass as pointer
// So, you use like so:
// LL_REMOVE(LL*, int (*comp)(void *, void *), <number>);
//
// An example of function to compare two integers would be like:
// 
// int compare(void *data, void *ctx) {
//     return *(int*)data == *(int*)ctx;
// }
#define LL_REMOVE(ll, compare, value) \
    { \
        __typeof__(value) _tmp = value; \
        ll_remove((ll), (compare), &_tmp); \
    }

// This macro helps you to add a new value without need create an extra variable
#define LL_ADD(ll, value) \
    { \
        __typeof__(value) _tmp = (value); \
        ll_add((ll), &_tmp, sizeof(__typeof__(value))); \
    }

typedef struct LLNode LLNode;

struct LLNode {
  void *data;
  LLNode *next;
};

typedef struct {
  LLNode *root;
  LLNode *tail;
  size_t length;
} LL;

LL *ll_new();
void ll_add(LL *ll, void *data, size_t data_size);
int ll_remove(LL *ll, int (*comp)(void *, void *), void *ctx);
void ll_free(LL *ll);

#endif // AOC_LL_H_

#ifndef LL_H_
#define LL_H_

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
void ll_free(LL *ll);

#endif // LL_H_

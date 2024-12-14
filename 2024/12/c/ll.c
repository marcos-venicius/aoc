#include <stdlib.h>
#include <string.h>
#include "ll.h"

LL *ll_new() {
    return calloc(1, sizeof(LL));
}

void ll_add(LL *ll, void *data, size_t data_size) {
    ll->length++;

    LLNode *node = malloc(sizeof(LLNode));

    node->data = malloc(data_size);
    node->next = NULL;

    memcpy(node->data, data, data_size);

    if (ll->root == NULL) {
        ll->root = node;
        ll->tail = node;
    } else {
        ll->tail->next = node;
        ll->tail = ll->tail->next;
    }
}

void ll_free(LL *ll) {
    if (ll->root == NULL) {
        free(ll);

        return;
    }

    LLNode *current = ll->root;

    while (current != NULL) {
        LLNode *next = current->next;

        free(current->data);
        free(current);

        current = next;
    }

    free(ll);
}

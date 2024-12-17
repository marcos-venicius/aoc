#include "../include/lib/ll.h"
#include <stdlib.h>
#include <assert.h>
#include <string.h>

LL *ll_new() {
    return calloc(1, sizeof(LL));
}

void ll_add(LL *ll, void *data, size_t data_size) {
    assert(ll != NULL);
    assert(data != NULL);
    assert(data_size > 0);

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

int ll_remove(LL *ll, int (*comp)(void *, void *), void *ctx) {
    assert(ll != NULL);

    LLNode *slow = NULL;
    LLNode *fast = ll->root;

    while (fast != NULL) {
        if (comp(fast->data, ctx) == 1) {
            if (slow == NULL) {
                LLNode* next = ll->root->next;

                free(ll->root->data);
                free(ll->root);

                ll->root = next;

                if (ll->root->next == NULL) {
                    ll->tail = ll->root;
                }
            } else {
                slow->next = fast->next;

                free(fast->data);
                free(fast);

                if (slow->next == NULL) {
                    ll->tail = slow;
                }
            }

            ll->length--;

            return 1;
        }

        slow = fast;
        fast = fast->next;
    }

    return 0;
}

void ll_free(LL *ll) {
    if (ll == NULL) return;

    if (ll->root == NULL) {
        free(ll);

        return;
    }

    LLNode *current = ll->root;

    while (current != NULL) {
        LLNode *next = current->next;

        if (current->data != NULL) {
            free(current->data);
        }

        free(current);

        current = next;
    }

    free(ll);
}

#include "../include/ll.h"
#include <stdio.h>

int compare(void *data, void *ctx) {
    return *(int*)data == *(int*)ctx;
}

int main() {
    LL *ll = ll_new();

    LL_ADD(ll, 10);
    LL_ADD(ll, 20);
    LL_REMOVE(ll, compare, 10);

    LLNode *current = ll->root;

    while (current != NULL) {
        printf("%d\n", *(int*)current->data);
        current = current->next;
    }

    ll_free(ll);

    return 0;
}

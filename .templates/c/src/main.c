#include "../include/lib/ll.h"
#include "../include/lib/map.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>

int main() {
    LL *ll = ll_new(free, NULL);

    ll_add_i(ll, 10);
    ll_add_i(ll, 20);
    ll_add_i(ll, 1255);
    ll_add_s(ll, "hello, my name is marcos");
    ll_add_s(ll, "lorem ipsum dolor sit ammet consectur");

    ll_remove_by_index(ll, 1);

    int *a = ll_find_by_index(ll, 0);
    int *b = ll_find_by_index(ll, 1);
    char *c = ll_find_by_index(ll, 2);
    char *d = ll_find_by_index(ll, 3);

    printf("index 0: %d\n", *a);
    printf("index 1: %d\n", *b);
    printf("index 2: %s\n", c);
    printf("index 3: %s\n", d);
    printf("Count: %ld\n", ll->count);

    ll_free(ll);

    return 0;
}

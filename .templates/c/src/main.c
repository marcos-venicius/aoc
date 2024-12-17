#include "../include/lib/ll.h"
#include "../include/lib/map.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>

int compare(void *data, void *ctx) {
    return *(int*)data == *(int*)ctx;
}

int main() {
    LL *ll = ll_new();
    Map *map = map_new();

    LL_ADD(ll, 10);
    LL_ADD(ll, 20);
    LL_REMOVE(ll, compare, 10);

    LLNode *current = ll->root;

    while (current != NULL) {
        printf("%d\n", *(int*)current->data);
        current = current->next;
    }

    map_set_i(map, "test", 10);
    map_set_i(map, "test", 20);
    map_set_i(map, "testing", 30);

    map_set_string(map, "message", "hello world");
    map_set_string(map, "message", "hello world asdlfkjasdfl asdlk jsdf");

    char *message = map_get(map, "message");
    int *n = map_get(map, "test");
    int *n2 = map_get(map, "testing");

    printf("test: %d\n", *n);
    printf("testing: %d\n", *n2);
    printf("message: %s\n", message);
    printf("%ld\n", map->length);
    assert(map->length == 3);

    map_free(map);
    ll_free(ll);

    return 0;
}

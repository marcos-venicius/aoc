#include "../include/lib/ll.h"
#include "../include/lib/map.h"
#include <stdio.h>
#include <string.h>

int main() {
    LL *ll = ll_new(NULL, NULL);

    ll_free(ll);

    return 0;
}

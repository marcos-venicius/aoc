#!/usr/bin/env python3

import hashlib, itertools, multiprocessing, re

FILE = 'input.txt'
PASS_SIZE = 8
CHUNK_SIZE = 500_000


def scan_chunk(args):
    door, start = args
    base = hashlib.md5(door)
    hits = []

    for index in range(start, start + CHUNK_SIZE):
        h = base.copy()
        h.update(b'%d' % index)
        d = h.digest()

        if d[0] or d[1] or d[2] > 0x0f:
            continue

        hits.append((d[2], d[3] >> 4))

    return hits


def main():
    door = re.sub(r'\s', '', open(FILE, 'r').read()).encode('utf-8')

    part_one = []
    part_two = [0] * PASS_SIZE
    part_two_indexes = set()

    chunks = ((door, start) for start in itertools.count(0, CHUNK_SIZE))

    with multiprocessing.Pool() as pool:
        # imap returns the chunks in order, which both parts depend on.
        for hits in pool.imap(scan_chunk, chunks):
            for sixth, seventh in hits:
                if len(part_one) < PASS_SIZE:
                    part_one.append(f'{sixth:x}')

                if sixth < len(part_two) and sixth not in part_two_indexes:
                    part_two[sixth] = f'{seventh:x}'
                    part_two_indexes.add(sixth)

            if len(part_one) == PASS_SIZE and len(part_two_indexes) == PASS_SIZE:
                break

    print('P1:', ''.join(part_one))
    print('P2:', ''.join(part_two))

if __name__ == '__main__':
    main()

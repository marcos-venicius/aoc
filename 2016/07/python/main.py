#!/usr/bin/env python3

import re

INPUT = './input.txt'

def dissect_ip(ip):
    chunks = []

    for char in ip:
        if char == '[':
            chunks.append(['+'])
        elif char == ']':
            chunks.append(['-'])
        else:
            if len(chunks) == 0:
                chunks.append(['-'])

            chunks[-1].append(char)

    return [''.join(chunk) for chunk in filter(lambda x: len(x) > 0, chunks)]

def get_abas(seq):
    if len(seq) < 3:
        return []

    out = []

    for i in range(len(seq)):
        if i + 2 >= len(seq):
            break

        if seq[i] == seq[i + 2] and seq[i] != seq[i + 1]:
            out.append(seq[i:i+3])

    return out

def has_abba(seq):
    if len(seq) < 4:
        return False

    for i in range(len(seq)):
        if i + 3 >= len(seq):
            break

        if seq[i] == seq[i+1]:
            continue

        # 0 1 2 3 4 5
        # a b b a x x
        # ^
        # i

        if seq[i] == seq[i+3] and seq[i+1] == seq[i+2]:
            return True

    return False

def get_aba_reverse(aba):
    a = aba[0]
    b = aba[1]

    return f'{b}{a}{b}'

def supports_ssl(ip):
    supernet = set()
    hypernet = set()

    for chunk in ip:
        abas = get_abas(chunk[1:])

        if chunk[0] == '-':
            supernet.update(abas)
        else:
            hypernet.update(abas)

    return any(get_aba_reverse(aba) in hypernet for aba in supernet)

def supports_tls(ip):
    contains_abba = False

    for chunk in ip:
        if chunk[0] == '+':
            if has_abba(chunk[1:]):
                return False
        elif chunk[0] == '-':
            if has_abba(chunk[1:]):
                contains_abba = True
        else:
            raise Exception(f'surely I did something realllly wrong: "{chunk}"')

    return contains_abba

ips = list(map(dissect_ip, list(filter(lambda x: x != '', re.split(r'\s', open(INPUT, 'r').read())))))

part_one = len(list(filter(supports_tls, ips)))
part_two = len(list(filter(supports_ssl, ips)))

print('P1:', part_one)
print('P2:', part_two)

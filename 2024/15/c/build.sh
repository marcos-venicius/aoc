#!/usr/bin/env bash

clang -Wall -Wextra -ggdb -pedantic -I$PWD/raylib/include/ -Wl,-rpath=$PWD/raylib/lib/ -L$PWD/raylib/lib/ -lraylib -lm -o 15 main.c

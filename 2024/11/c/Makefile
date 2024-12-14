CXX = gcc
CXX_FLAGS = 
DEBUG_FLAGS = -Wall -Wextra -pedantic -g -fsanitize=address

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

ifeq ($(DEBUG), 1)
	CXX_FLAGS += $(DEBUG_FLAGS)
else
	CXX_FLAGS += -s -O2
endif

aoc: $(OBJ)
	$(CXX) $(CXX_FLAGS) -o $@ $^

%.o: %.c
	$(CXX) $(CXX_FLAGS) -c $< -o $@

clean:
	rm -rf debug aoc *.o

CXX = gcc
CXX_FLAGS = -s -O2 -DNDEBUG
DEBUG_FLAGS = -g -DDEBUG -Wall -Wextra

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

aoc: $(OBJ)
	$(CXX) $(CXX_FLAGS) -o $@ $^

debug: $(OBJ)
	$(CXX) $(DEBUG_FLAGS) -o $@ $^

sanitize: $(OBJ)
	$(CXX) $(DEBUG_FLAGS) -fsanitize=address -o $@ $^

%.o: %.c
	$(CXX) -c $< -o $@

clean:
	rm -rf aoc debug sanitize *.o

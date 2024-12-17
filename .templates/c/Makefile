CXX = gcc
CXX_FLAGS = -g -fsanitize=address -Wall -Wextra -pedantic

SRC=$(wildcard **/*.c)
OBJS=$(SRC:%.c=%.o)

aoc: $(OBJS)
	$(CXX) $(CXX_FLAGS) -o $@ $^

%.o: %.c
	$(CXX) $(CXX_FLAGS) -c $< -o $@

clean:
	rm -rf aoc $(OBJS)

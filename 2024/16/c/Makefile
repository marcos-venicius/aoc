CLIBS = ../../../clibs
CXX = clang
CXX_FLAGS = -Wall -Wextra -ggdb -pedantic -I$(CLIBS)/raylib/include/ -Wl,-rpath=$(CLIBS)/raylib/lib/ -L$(CLIBS)/raylib/lib/ -lraylib -lm

all: one two

one: one.o io.o aoc.o
	$(CXX) $(CXX_FLAGS) -o one $^

two: two.o io.o aoc.o
	$(CXX) $(CXX_FLAGS) -o two $^

%.o: %.c
	$(CXX) $(CXX_FLAGS) -c $< -o $@

clean:
	rm -rf one two *.o

CLIBS = ../../../clibs
CXX = clang
CXX_LIBS = -I$(clibs)/ll/include/ -L$(CLIBS)/ll -I$(CLIBS)/raylib/include/ -Wl,-rpath=$(CLIBS)/ll/ -Wl,-rpath=$(CLIBS)/raylib/lib/ -L$(CLIBS)/raylib/lib/ -lll -lraylib -lm
CXX_FLAGS = -Wall -Wextra -ggdb -pedantic

all: one two

one: one.o io.o aoc.o
	$(CXX) $(CXX_FLAGS) $(CXX_LIBS) -o one $^

two: two.o io.o aoc.o
	$(CXX) $(CXX_FLAGS) $(CXX_LIBS) -o two $^

%.o: %.c
	$(CXX) $(CXX_FLAGS) $(CXX_LIBS) -c $< -o $@

clean:
	rm -rf one two *.o

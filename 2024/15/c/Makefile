CLIBS = ../../../clibs
CXX = clang
CXX_FLAGS = -Wall -Wextra -ggdb -pedantic -I$(CLIBS)/raylib/include/ -Wl,-rpath=$(CLIBS)/raylib/lib/ -L$(CLIBS)/raylib/lib/ -lraylib -lm


all: one two

one: clean
	$(CXX) $(CXX_FLAGS) -o one one.c

two: clean
	$(CXX) $(CXX_FLAGS) -o two two.c

clean:
	rm -rf one two

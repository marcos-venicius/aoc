CXX = clang
CXX_FLAGS = -Wall -Wextra -ggdb -pedantic -I$(PWD)/raylib/include/ -Wl,-rpath=$(PWD)/raylib/lib/ -L$(PWD)/raylib/lib/ -lraylib -lm


all: one two

one:
	$(CXX) $(CXX_FLAGS) -o one one.c

two:
	$(CXX) $(CXX_FLAGS) -o two two.c

clean:
	rm -rf one two

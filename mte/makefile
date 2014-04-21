CC = gcc
TARGETS = mte
CFLAGS = -std=c99

all: $(TARGETS)

mte: mte.c
	@ echo "compile: mte"
	@ $(CC) -o mte mte.c $(CFLAGS)

clean:
	@ rm $(TARGETS) && echo "remove: $(TARGETS)"


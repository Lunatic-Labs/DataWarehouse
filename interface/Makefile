CC = gcc
CFLAGS = -I. -std=c11 -Wall -Wextra
LDFLAGS = -lcurl
DEPS = datawarehouse_interface.h
OBJ = main.o datawarehouse_interface.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

.PHONY: clean

clean:
	rm -f *.o main

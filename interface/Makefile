CC = gcc
CFLAGS = -I. -lcurl
DEPS = datawarehouse_interface.h
OBJ = main.o datawarehouse_interface.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f *.o main

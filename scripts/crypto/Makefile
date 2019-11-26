SRCS =
OBJS = $(SRCS:.cpp=.o)
TARGET = restrictSHA1
CFLAGS = -std=c++11 -O2 -I ../core/

CFLAGS += $(MACROS)

.cpp.o: $(SRCS)
	g++ -c $< -o $@ $(CFLAGS)

all: $(OBJS) $(TARGET).cpp
	g++ $(OBJS) $(CFLAGS) $(TARGET).cpp -o $(TARGET)

clean:
	rm -f $(OBJS) $(TARGET) *.o
	rm -rf ./generated/

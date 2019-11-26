SRCS =
OBJS = $(SRCS:.cpp=.o)
RESTRICT_TARGET = restrictSHA1
HARVEST_TARGET = harvestResults

CFLAGS = -std=c++11 -O2 -I ../core/

CFLAGS += $(MACROS)

.cpp.o: $(SRCS)
	g++ -c $< -o $@ $(CFLAGS)

all: $(OBJS) $(RESTRICT_TARGET).cpp
	g++ $(OBJS) $(CFLAGS) $(RESTRICT_TARGET).cpp -o $(RESTRICT_TARGET)
	g++ $(OBJS) $(CFLAGS) $(HARVEST_TARGET).cpp -o $(HARVEST_TARGET)

clean:
	rm -f $(OBJS) $(RESTRICT_TARGET) $(HARVEST_TARGET) *.o

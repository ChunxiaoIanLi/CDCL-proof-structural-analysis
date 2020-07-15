# Names of tools to use when building
CXX = g++
LD  = g++
RM  = rm -rf

# Warnings to be raised by the CPP compiler
WARNS = -Wall

# Compiler and linker flags
CPPFLAGS = -g -O3 -std=c++17 $(WARNS)
LDFLAGS = -s

# Source files
SRC_DIR = .
SRCS = \
	$(wildcard $(SRC_DIR)/*.cpp)

# Object files
OBJS = $(foreach SRC, $(subst .cpp,.o,$(SRCS)), $(SRC:$(SRC_DIR)/%=%))

TARGET = countResolvable

.PHONY: all clean

all: $(OUT_DIR) $(OBJ_DIR) $(TARGET) 

run: $(TARGET)
	$(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(CPPFLAGS) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CPPFLAGS) -c $< -o $@

clean:
	$(RM) $(TARGET) *.o


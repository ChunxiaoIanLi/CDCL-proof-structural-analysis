# Names of tools to use when building
CXX = g++
LD  = g++
RM  = rm -rf

# Warnings to be raised by the CPP compiler
WARNS = -Wall

# Compiler and linker flags
CPPFLAGS = -O3 -std=c++17 -fPIC -I../../../python2.7/ $(WARNS)
LDFLAGS = -s

# Source files
SRC_DIR = src
MAIN_SRC = main.cpp
PYTHON_BINDING_SRC = pythonBindings.cpp
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Object files
MAIN_OBJ = $(subst .cpp,.o,$(MAIN_SRC))
PYTHON_BINDING_OBJ = $(subst .cpp,.o,$(PYTHON_BINDING_SRC))
OBJS = $(subst .cpp,.o,$(SRCS))

MAIN_TARGET = countResolvable
PYTHON_BINDING_TARGET = libmergeability.so

.PHONY: all clean

$(MAIN_TARGET): $(OBJS) $(MAIN_OBJ)
	$(CXX) $(CPPFLAGS) -o $(MAIN_TARGET) $(MAIN_OBJ) $(OBJS) $(LDFLAGS)

python: $(PYTHON_BINDING_TARGET)

$(PYTHON_BINDING_TARGET): $(OBJS) $(PYTHON_BINDING_OBJ)
	$(CXX) -shared -Wl,-soname,$(PYTHON_BINDING_TARGET) -o $(PYTHON_BINDING_TARGET) $(PYTHON_BINDING_OBJ) $(OBJS) -lpython2.7

$(PYTHON_BINDING_OBJ):
	$(CXX) $(CPPFLAGS) -c $(PYTHON_BINDING_SRC) -o $(PYTHON_BINDING_OBJ)

%.o: %.cpp
	$(CXX) $(CPPFLAGS) -c $< -o $@

clean:
	$(RM) $(MAIN_TARGET) $(PYTHON_BINDING_TARGET) $(MAIN_OBJ) $(PYTHON_BINDING_OBJ) $(SRC_DIR)/*.o


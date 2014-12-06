CWD=$(shell pwd)
CC= g++
CFLAGS = -g -Wall -std=c++0x
CFLAGS2 = -g -Wall
MAIN = main

LIB_PATH = -L/usr/lib
INCLUDES = -I/usr/include/boost/iostreams
LIBRERIAS = -lboost_iostreams

TARGET = $(MAIN)
OBJS = $(shell ls ./*.cpp | grep -v test | sed s/.cpp/.o/)


ALL_TEST = $(shell ls ./*test.cpp | sed s/.cpp//)
TEST_OBJS = $(shell ls ./*.h | grep -v main | grep -v test | sed s/.h/.o/)
DEPEN_TEST = $(shell ls ./*.h | grep -v test)
#TEST_OBJS = Modelo.o Estadisticas.o
#DEPEN_TEST = Modelo.h Estadisticas.h
#DEPEN_TEST = $(shell grep '.h' Ejemplo1test.cpp | sed 's/\#include \"//' | sed s/\"// | sed s/.h/.o/)
#DEPEN_TEST = $(shell echo $(GREP) | sed 's/#include //')
#$(shell grep *.h Ejemplo1test.cpp | sed 's/#include //' | sed s/\"// | sed s/\"//)
#DEPEN_TEST =  $(shell grep .h\" *test.cpp)
#NEWVAR =  `awk '{print $2\}')'
# | sed s/\"// | sed s/\"//)

all: $(TARGET)
	@echo "Termine de compilar el programa principal"

$(TARGET) : $(OBJS)
	$(CC) $(CFLAGS) $^ -o $(TARGET) $(INCLUDES) $(LIB_PATH) $(LIBRERIAS)

%.o : %.cpp %.h
	$(CC) $(CFLAGS) -c $< -o $@

%.o : %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# previene hacer algo con fichero llamado clean
.PHONY: clean 

clean:
	rm -rf *.o *~ $(TARGET) $(ALL_TEST) core

test: $(ALL_TEST)
	@echo "Termine de compilar los test"	

%test: %test.cpp $(TEST_OBJS) $(DEPEN_TEST) 
	$(CC) $(CFLAGS) $^ -o $@ $(INCLUDES) $(LIB_PATH) $(LIBRERIAS)







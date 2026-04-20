all:
	make socket.o
	make select.o
	make connections.o
	
socket.o: socket.h socket.cc
	g++ -c socket.cc

select.o: select.h select.cc
	g++ -c select.cc

connections.o: connections.h connections.cc
	g++ -c connections.cc

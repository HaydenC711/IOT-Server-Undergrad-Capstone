app:
	make projserver
	
projserver: projserver.o devices.o apps.o accountStruct.o tools/socket.o tools/select.o tools/connections.o
	g++ -o projserver projserver.o devices.o apps.o accountStruct.o tools/socket.o tools/select.o tools/connections.o	
	
projserver.o : projserver.cc packet.h
	g++ -c -I tools projserver.cc

devices.o : devices.cc devices.h packet.h tools/socket.h
	g++ -c -I tools devices.cc
	
apps.o : apps.cc apps.h packet.h tools/socket.h
	g++ -c -I tools apps.cc
	
accountStruct.o : accountStruct.cc accountStruct.h 
	g++ -c -I tools accountStruct.cc
		
clean:
	rm -f *.o

	
projserver2: projserver2.o devices.o apps.o tools/socket.o tools/select.o tools/connections.o
	g++ -o projserver2 projserver2.o devices.o apps.o tools/socket.o tools/select.o tools/connections.o
	
projserver2.o : projserver2.cc packet.h
	g++ -c -I tools projserver2.cc
	
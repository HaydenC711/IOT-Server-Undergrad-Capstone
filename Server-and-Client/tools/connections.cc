#include "connections.h"
#include <stdlib.h>

Connections::Connections(int maxConnections)
{
  MaxConnections = maxConnections;
  NumConnections = 0;
  IterIndex = -1;
  TheConnections = new Socket * [maxConnections];  
  ClientData = new void * [maxConnections];
}
  

Connections::~Connections()
{
  free(TheConnections);
  free(ClientData);
  MaxConnections = 0;
  NumConnections = 0;
}
  

// helper method
int 
Connections::findSocket(int fd)
{
  int i = 0; 
  while(i < NumConnections) {
    if(TheConnections[i]->fd() == fd) 
      return i;
    i++;
  }
  
  return -1;
}



bool 
Connections::addClient(Socket *socket)
{
   // Reset the iterator index if a new client is added.
  IterIndex = -1;
  
   // The container is full.
  if(NumConnections == MaxConnections) 
    return false;
  
   // Make sure the socket is not already in the container.
  int ndx = findSocket(socket->fd());
  if(ndx >= 0) 
    return false;
  
  TheConnections[NumConnections] = socket;
  ClientData[NumConnections] = NULL;
  NumConnections++;
  return true;
}


bool 
Connections::removeClient(int fd)
{
   // Reset the iterator index if a client is removed.
  IterIndex = -1;
  
  int ndx = findSocket(fd);
  if(ndx < 0)
    return false;
  
  TheConnections[ndx] = TheConnections[NumConnections - 1];
  TheConnections[NumConnections - 1] = NULL;
  
  ClientData[ndx] = ClientData[NumConnections - 1];
  ClientData[NumConnections - 1] = NULL;
  
  NumConnections--;      
  return true;
}


Socket * 
Connections::getClient(int fd)
{
  int ndx = findSocket(fd);
  
  if(ndx < 0) 
    return NULL;
  else
    return TheConnections[ndx];
}


Socket *
Connections::firstClient()
{
  IterIndex = 0;  
  return nextClient();
}


Socket *
Connections::nextClient()
{
  if(IterIndex < 0 || IterIndex >= NumConnections)
    return NULL;
  
  Socket *client = TheConnections[IterIndex];
  IterIndex++;
  return client;  
}


bool 
Connections::addData(int fd, void *data)
{
  int ndx = findSocket(fd);
  
  if(ndx < 0)
    return false;
  else { 
    ClientData[ndx] = data;
    return true;
  }  
}


bool 
Connections::removeData(int fd)
{
  int ndx = findSocket(fd);
  
  if(ndx < 0)
    return false;
  else { 
    ClientData[ndx] = NULL;
    return true;
  }  
  
}


void * 
Connections::getData(int fd)
{
  int ndx = findSocket(fd);
  
  if(ndx < 0)
    return NULL;
  else 
    return ClientData[ndx];
}


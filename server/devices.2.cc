#include "devices.h"
#include "packet.h"
#include "clientInfo.h"
#include "connections.h"
#include "socket.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

ServerSocket devServer;
Connections devClientList(200);


int configDevices(int port)
{
    /* Bind the server listening sockets to the given port. */
  if(devServer.bind(port)) {
    printf("Device server bound to port #%d\n", port);
    return devServer.fd();
  }
  else {
    printf("Error: the device socket could not be bound to port #%d\n", port);
    return -1;
  }  
}


bool isDevice(int fd)
{
  Socket *theClient = devClientList.getClient(fd);
  return theClient != NULL;
}


void endDevServer()
{
  devServer.close();
}


bool sendDevRequest(Socket *client, Packet *packet)
{
  client->send(packet, sizeof(Packet));
  
  int nbytes = client->recv(packet, sizeof(Packet));
  
  if(nbytes <= 0) {
    disconnectDev(client);
    return true;
  }
  else
    return false;
}


int getUsersDevices(int acctNum, int fdList[])
{
  return 0;
}


void disconnectDev(Socket *client)
{
  int fd = client->fd();
  
   /* Remove the device data and socket from the list. */
  devClientList.removeData(fd);
  devClientList.removeClient(fd);
    
   /* Close the socket and delete the object. */
  client->close();
  delete client;  
}

 
int handleDevConnection()
{
  printf("device function triggered\n");
  Socket *client = devServer.accept();
  printf("Device connection from: %s on port #%d\n", 
          client->address(), client->port());
  
  ClientInfo *info = new ClientInfo;
  info->appConnection = false;
  info->authenticated = false;
  info->acctNumber = 0;
  
  bool add = devClientList.addClient(client);
  devClientList.addData(client->fd(), info);
       
  return client->fd();
}
  
  


bool handleDevPacket(int fd)
{
	//lightbulb protocol
		//Send signal given by main application
		//sever accepts traffic from lightbulb
		//create traffic report		
  
  Socket *client;
  ClientInfo *info;

   /* Get the client socket and data. */
  client = devClientList.getClient(fd);
  info = (ClientInfo * ) devClientList.getData(fd);
    
  DevPacket packet;
  int nbytes = client->recv(&packet, sizeof(packet));
  
  if(nbytes <= 0) {
    disconnectDev(client);
    return true;
  }
  else {    
    printf("Packet received (%d)\n", nbytes);
    printf("op = %d, dev = [%s], param = %d\n", 
            packet.opcode, packet.devId, packet.param);
    
    if(packet.opcode == DEV_CONN) {
      // if a valid dev id, then authenticate the device by setting the
      // account number in the info struct.
      info->authenticated = true;
    }
    else {
       /* If the device has not authenticated with the server, 
          disconnect the device. */
      if(!info->authenticated) {
        disconnectDev(client);
        return true;
      }                  
    }
  }
  
  return false;
}


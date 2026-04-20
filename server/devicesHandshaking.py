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
  info->acctNumber = 0;
  
  bool add = devClientList.addClient(client);
  devClientList.addData(client->fd(), info);
    
  
  DevPacket packet;
    
 
  //if the client couldn't be added, close the connection
  if (!add) {
  	  printf("Failure to complete client connection\n");
   	  client->close();
  }
   
  printf("Host Connection Successful\n");
   
  //Start Handshaking
  //send START 
 // packet.opcode = 0;
  //strcmp(packet.devId, "NONE");
  //packet.padding = "";
  printf("Sending handshaking message\n");
  strcpy(packet.handshake, "START\n");
  client->send(&packet, sizeof(packet));
  printf("Waiting for handshaking response\n");

  //recieve the response
  int data = client->recv(&packet, sizeof(packet));
  //printf("data = %d\n",  sizeof(packet));
  printf("opcode: %d\n", packet.opcode);
  //printf("message: %s\n", packet.handshake);
  printf("\nMAC Address: %s\n", packet.devId);

  if (strcmp(packet.handshake, "\rHI") == 0){
   	  //printf("packet message: %s\n", packet.message);
   	  printf("Handshake complete\n");
  }
  
  //delete client if handshake failed
  else{
  	  printf("packet message: %s\n", packet.handshake);
  	  printf("packet message length: %d\n", sizeof(packet.handshake));
  	  
  	  printf("Handshake failed\n");
  	  devClientList.removeData(client->fd());
  	  devClientList.removeClient(client->fd());
  	  client->close();
  	  delete info;
  	  delete client;
  	  return -1;
  }
  

  //if (info.appConnection == false){
  	   //Ask the user to login in to add the application
  	       // only give the user 3 attempts then terminate the connection
  	   //upon successful login, prompt for the passphrase
 // }
  
  
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
  }
  
  return false;
}


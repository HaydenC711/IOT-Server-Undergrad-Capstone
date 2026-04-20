#include "devices.h"
#include "apps.h"
#include "packet.h"
//#include "clientInfo.h"
#include "connections.h"
#include "socket.h"
#include "accountStruct.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


ServerSocket devServer;
Connections devClientList(200);

Connections getConnectedDevices(){
	return devClientList;
}

const int DEV_CONN = 100;
const int DEV_OK = 101;
const int DEV_REPLY = 102;
const int DEV_DISCONNECT = 103;

const int DEV_LIGHT = 10000;

int getDeviceFd(char *devId){
	
	//printf("devlist len: %d\n", sizeof(devList));

	//printf("sizof dev: %d\n", sizeof(devClientList));
	//Search through devList and find the fd of the device with given device id

	Socket *curClient = devClientList.firstClient();
	//printf("sizeOf(devList): %d\n", sizeof(devClientList));
	int fd = -1;
	while (curClient != NULL) {
		fd = curClient->fd();
		//printf("fd for device: %d\n", fd);
		ClientInfo *info = new ClientInfo;
		info = (ClientInfo * ) devClientList.getData(fd);
		//printf("devId needed: %s\n", devId);
		//printf("devId of current device: %s\n", info->devId);
		//printf("devId needed len %d\n", strlen(devId));
		//printf("devId of current %d\n", strlen(info->devId));
		if (strcmp(info->devId, devId) == 0) {
			return fd;
		}
		curClient = devClientList.nextClient();
	}
	//printf("Failed to find fd\n");
	return 0;
}

Socket * getTargetClient(int fd){
	ClientInfo *info1 = new ClientInfo;
	info1 = (ClientInfo * ) devClientList.getData(fd);
	//printf("devId: %s", info1->devId);
	return devClientList.getClient(fd);
	
}

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


bool sendDevRequest(Socket *client, DevPacket *packet)
{
  client->send(packet, sizeof(packet));
  
  int nbytes = client->recv(packet, sizeof(packet));
  
  if(nbytes <= 0) {
    //disconnectDev(fd);
    return true;
  }
  else
    return false;
}

//Can use socket (client) instead of fd as parmeter
//This was changed during debugging
//Anytime this function is used, return true; must be the following line
void disconnectDev(int fd){
	//exit(1);
	printf("Disconnecting Device\n");
  //int fd = client->fd();
  //printf("fd: %d", fd);
   /* Remove the device data and socket from the list. */
  Socket *client = devClientList.getClient(fd);
  devClientList.removeData(fd);
  devClientList.removeClient(fd);

   /* Close the socket and delete the object. */
  client->close();
  delete client;
 
}

 
int handleDevConnection()
{
  //printf("device function triggered\n");
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
  
  

//handles packets from the device
bool handleDevPacket(int fd)
{
  Socket *client;
  ClientInfo *info;

   /* Get the client socket and data. */
  client = devClientList.getClient(fd);
  info = (ClientInfo * ) devClientList.getData(fd);
    
  DevPacket packet;
  int nbytes = client->recv(&packet, sizeof(packet));
  
  if(nbytes <= 0) {
    disconnectDev(fd);
    return true;
  }
  else {    
    //printf("Packet received (%d)\n", nbytes);
    //printf("op = %d\n", packet.opcode);
    //printf("dev = %s\n", packet.devId);
    //printf("param = %d\n", packet.param);
    
    if(int(packet.opcode) == DEV_CONN) {
      // if a valid dev id, then authenticate the device by setting the
      // account number in the info struct.
      //Should check if devId is in struct
      int num = checkDevId(packet.devId);
      if (num == 0){
      	  packet.opcode = 103;
	  	  client->send(&packet, sizeof(packet));
	  	  disconnectDev(fd);
	  	  return true;
	  	  //send instruction
	  	  //disconnect device**/
      	  
		  
	  }
	  else {
	  	  info->authenticated = true;
		  
		  info->acctNumber = findAccountNum(packet.devId);
		  //printf("\n\n");
		  //printf("Fd of this device (): %d\n", fd);
		  //printf("Account number of account device is connected to: %d\n", info->acctNumber);
		  
		  //send response to the device
		  //printf("Sending successful connection response\n");
		  
		  //printf("packet.devId: %s\n", packet.devId);
		  //strcat(packet.devId, "\0");
		  strcpy(info->devId, packet.devId);
		  //printf("info->devId: %s\n", info->devId);
		  packet.opcode = 101;
		  client->send(&packet, sizeof(packet));
		  //printf("packet.devId len %d\n", strlen(packet.devId));
		  //printf("info->devId len %d\n", strlen(info->devId));
	  }
    }
    
    else {
    	//printf("Entering Else\n");
       /* If the device has not authenticated with the server, 
          disconnect the device. */
      if(!info->authenticated) {
      	  //printf("Entering not authenticated\n");
        disconnectDev(fd);
        
       
        //send response to the device
        //printf("Sending failed connection response\n");
        packet.opcode = -1;
        client->send(&packet, sizeof(packet));
        return true;
        
      //deal with other opcodes and send the packet to the associated main application
      //May not even have to handle them separately
      }
      //activated for queries
      else if (packet.opcode == DEV_REPLY) {
      	  if (packet.param == 1 || packet.param == 0) {
      	  
			  //search through applist and grab fd
			  
			  int fd = getAppFd(packet.devId);
			  
			  //printf("Final fd for app: %d\n", fd);

			  Socket *app = getTargetApp(fd);
			  
			  app->send(&packet, sizeof(packet));
			  
			  //printf("sending to main app\n");
      	  }
      	  //Grab account number from accountstruct (findAccountNum(packet.devId)
      	  //or maybe we include the accountnumber in the packet?
      }
      
      else if (packet.opcode == DEV_OK) {
      	  //printf("We in Dev_ok\n");
       	   //send packet to main application
       	   //search through applist and grab fd
       	   int fd = getAppFd(packet.devId);
       	   //printf("Final fd for app: %d\n", fd);
       	   Socket *app = getTargetApp(fd);
       	   app->send(&packet, sizeof(packet));
       	   
       	   //printf("sending to main app\n");
      }
      
      else if (packet.opcode == DEV_DISCONNECT) {
      	  printf("Client Disconnected\n");
      	  disconnectDev(fd);
      	  return true;
      	  
      }
   
        
    }                  
  }
  
  //return false if the device wasn't disconnected
  return false;
}




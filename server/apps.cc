#include "devices.h"
#include "packet.h"
//#include "clientInfo.h"
#include "connections.h"
#include "socket.h"
#include "accountStruct.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

ServerSocket appServer;
Connections appClientList(200);


int configApps(int port)
{
    /* Bind the server listening sockets to the given port. */
  if(appServer.bind(port)) {
    printf("Application server bound to port #%d\n", port);
    return appServer.fd();
  }
  else {
    printf("Error: the application socket could not be bound to port #%d\n", port);
    return -1;
  }  
}


int getAppFd(char *devId){
	int account = findAccountNum(devId);
	//printf("Account Num: %d", account);
	//printf("devlist len: %d\n", sizeof(devList));
	
	//Search through devList and find the fd of the device with given device id
	Socket *curClient = appClientList.firstClient();
	//printf("sizeOf(appList): %d\n", sizeof(appClientList));
	int fd = -1;
	while (curClient != NULL) {
		//printf("\n");
		fd = curClient->fd();
		//printf("fd for app: %d\n", fd);
		ClientInfo *info = new ClientInfo;
		info = (ClientInfo * ) appClientList.getData(fd);
		//printf("accountNo needed: %d\n", account);
		//printf("accountNo of current app: %d\n", info->acctNumber);
	
		if (account == info->acctNumber) {
			return fd;
		}
		curClient = appClientList.nextClient();
	}
	//printf("Failed to find fd\n");
	return 0;
}

Socket * getTargetApp(int fd){
	return appClientList.getClient(fd);
}

void endAppServer()
{
  appServer.close();
}


void disconnectApp(Socket *client)
{
  int fd = client->fd();
  
   /* Remove the device data and socket from the list. */
  appClientList.removeData(fd);
  appClientList.removeClient(fd);
    
   /* Close the socket and delete the object. */
  client->close();
  delete client;  
  
}
 

int handleAppConnection()
{
  Socket *client = appServer.accept();
  printf("App connection from: %s on port #%d\n", 
          client->address(), client->port());
  
  ClientInfo *info = new ClientInfo;
  info->appConnection = true;
  info->acctNumber = 0;
  
  appClientList.addClient(client);
  appClientList.addData(client->fd(), info);
    
  return client->fd();  
}


bool handleAppPacket(int fd)
{
	
  Socket *client;
  ClientInfo *info;
  
  /* Get the client socket and data. */
  client = appClientList.getClient(fd);
  info = (ClientInfo * ) appClientList.getData(fd);
   
  //Waiting for packet from main application
  //printf("Waiting for packets to send to device...\n");
  DevPacket packet;
  int nbytes = client->recv(&packet, sizeof(packet));
  
  if(nbytes <= 0) {
    disconnectApp(client);
    return true;
  }
  else {    
    //printf("Packet received (%d)\n", nbytes);
   // printf("op = %d, dev = [%s], param = %d\n", packet.opcode, packet.devId, packet.param);
   
    //Setting the account number of the client info struct (occurs during login)
    if (packet.opcode == 202) {
    	//printf("Setting Account Number\n");
    	info->acctNumber = packet.param;
    }
    else if (packet.opcode == 203) {
    	//printf("Reloading the Account Struct\n");
    	clearData();
    	readUserData();
    }
    //Sending packet to device
    else if (packet.opcode == 10000||packet.opcode == 103){
    	
    	if(packet.param == 99 || packet.param == 1 || packet.param == 0 || packet.param ==-1){
			//printf("account No: %d", info->acctNumber);
			//printf("Before getting fd\n");
			int fd = getDeviceFd(packet.devId);
			//printf("FD: %d", fd);
			//printf("After getting fd\n");
			/**if (int(fd) != 0){
				//Get target device using fd and send the packet to device
				printf("Before getting target\n");
				Socket *device = getTargetClient(fd);
				printf("After getting target\n");
				device->send(&packet, sizeof(packet));
				//printf("IT SENT\n");
			}**/
			if (int(fd) == 0) {
				client->send(&packet, sizeof(packet));
			}
			else{
				//If int(fd) != 0
				//Get target device using fd and send the packet to device
				//printf("Before getting target\n");
				Socket *device = getTargetClient(fd);
				//printf("After getting target\n");
				device->send(&packet, sizeof(packet));
				//printf("IT SENT\n");
			}
		

		}
		
    }
   
  }
    
  //Recieve signals from main application (turn device on, generate traffic report)
	//IF generate traffic report sent
		//send traffic report to main application
		//have device send traffic to sever automatically?
		
  return false;
}




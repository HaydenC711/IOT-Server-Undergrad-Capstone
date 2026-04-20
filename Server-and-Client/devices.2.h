#ifndef _DEVICES_H
#define _DEVICES_H

#include "socket.h"

int configDevices(int port);

void endDevServer();

 /* Used by the app module to request info from a device and to receive the
    reponse from the device. */
bool sendDevRequest(Socket *client, Packet *packet);

bool isDevice(int fd);

 /* Go through the list of attached devices and get the fd's for each
    device that belongs to the given account. Returns the number of 
    connected devices for the given account. */
int getUsersDevices(int acctNum, int fdList[]);
  
 /* Called to disconnect and remove a device's socket and client data. */
void disconnectDev(Socket *client);
  
 /* Called when a device connects on the dev listening socket. */
int handleDevConnection();

 /* Called when a device packet arrives. */
bool handleDevPacket(int fd);



#endif


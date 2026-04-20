#ifndef __DEVICES_H
#define __DEVICES_H

#include "connections.h"
#include "socket.h"
void loadDevices();
int configDevices(int port);

void endDevServer();

bool isDevice(int fd);


  
 /* Called to disconnect and remove a device's socket and client data. */
void disconnectDev(int fd);
  
 /* Called when a device connects on the dev listening socket. */
int handleDevConnection();

 /* Called when a device packet arrives. */
bool handleDevPacket(int fd);

Connections getConnectedDevices();
int getDeviceFd(char *devId);
Socket * getTargetClient(int fd);
#endif


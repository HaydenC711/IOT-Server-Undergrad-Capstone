#ifndef __APPS_H
#define __APPS_H

#include "socket.h"

int configApps(int port);

void endAppServer();

 /* Called to disconnect and remove an app's socket and client data. */
void disconnectApp(Socket *client);
  
 /* Called when an app connects on the dev listening socket. */
int handleAppConnection();

 /* Called when an app packet arrives. */
bool handleAppPacket(int fd);

Socket * getTargetApp(int fd);

int getAppFd(char *devId);

#endif

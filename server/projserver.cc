#include "accountStruct.h"
#include "devices.h"
#include "apps.h"

#include "select.h"

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

//function prototypes


FDSet inputSet;

const int APP_PORT_NUMBER = 30000;
const int DEV_PORT_NUMBER = 30001;


int main(int argc, char *argv[])
{
    /* If the user supplies a port number at the command-line, use that as
     * the port number. Otherwise, use the default ports. */
  int appPortNum = APP_PORT_NUMBER;
  int devPortNum = DEV_PORT_NUMBER;
  
  if(argc == 3) {
    appPortNum = atoi(argv[1]);
    devPortNum = atoi(argv[2]);
  }
  else if(argc > 1) {
    fprintf(stderr, "Error: invalid number of arguments supplied.\n");
    fprintf(stderr, "   usage: projserver app-port dev-port\n\n");
    return 1;
  }
  
  int appServerFD;
  int devServerFD;
  
   /* Bind the device server socket and client list. */
  devServerFD = configDevices(devPortNum);
  if(devServerFD < 0) 
    return -1;
  else 
    inputSet.addFD(devServerFD);

   /* Bind the app server socket and client list. */
  appServerFD = configApps(appPortNum);
  if(appServerFD < 0) 
    return -1;
  else
    inputSet.addFD(appServerFD);


    /* The server repeatedly waits for a connection from a client, processes 
       the client request, and then closes the client connection. */
  readUserData();
  while( true ) {
    
     /* Wait for input on a socket. */
  	int *activeSet = inputSet.select();
    
  	int i = 0;
  	while(activeSet[i] >= 0) {
  	  //printf("server i=%d\n", i);
  	  int fd = activeSet[i];
  	  //printf("fd (in projserver): %d\n");
  	  if(fd == appServerFD) { 
  	    fd = handleAppConnection();
        inputSet.addFD(fd);   
        printf("App Connection Successful\n");  	    
  	  }
  	  else if(fd == devServerFD) {
  	    fd = handleDevConnection();
        inputSet.addFD(fd);   
        printf("Device Connection Successful\n");
  	  }
  	  else {  	
  	    bool closed;
  	    if(isDevice(fd)) {
  	      closed = handleDevPacket(fd);
  	      
  	    }
  	    else
  	      closed = handleAppPacket(fd);
  	      
  	     /* If the socket was closed, remove the fd from the inputSet. */
  	 
  	    if(closed) 
  	      inputSet.removeFD(fd);
  	  	
  	  }
  	  
  	  i++;
  	}
  }  
  
   /* This should be added to a ctrl-c handerler. */
  endDevServer();
  endAppServer();
}




/**void addDevice(struct Device newDevice) { //struct UserDetails *user, struct Device newDevice
    if (users->numDevices < MAX_DEVICES) {
        users->devices[users->numDevices] = newDevice;
        users->numDevices++;
    }
}**/




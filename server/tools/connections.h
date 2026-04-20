/* connctions.h
 *
 * Defines a container class for storing and managing a collection of
 * client socket connections. 
 *
 * R. Necaise 
 * January 2023
 */

#ifndef _CONNECTIONS_H
#define _CONNECTIONS_H

#include "socket.h"


class Connections {
public:
   /* Create the connection container that store a collection of client 
    * socket connections. maxConnections indicates the maximum number of 
    * connections that can be stored in the container. The default is 50. */ 
  Connections(int maxConnections = 50);
  
   /* Clears the container and releases the dynamic data it uses. */
  ~Connections();
  
   /* Returns the number of connection sockets stored in the container. */
  int numConnections() const { return NumConnections; }  // deprecated
  int numClients() const { return NumConnections; }
  
   /* Returns the maximum number of connections that can be stored. */
  int maxConnections() const { return MaxConnections; }  // deprecated
  int maxClients() const { return MaxConnections; }
  
   /* Add a client socket to the container. Returns true if the socket
      was added or false if the socket is already in the container or 
      there is insufficient space. */
  bool addClient(Socket *socket);

   /* Remove a client socket from the container based on the socket's
      file descriptor. The socket is not closed or deleted, just removed.
      Returns true if the socket was removed or false if the socket is not 
      in the container. */
  bool removeClient(int fd);

   /* Returns a pointer to the client socket object based on the socket's
      file descriptor. If the socket is not in the container, NULL is
      returned. */ 
  Socket * getClient(int fd);
  
  
  /* The two methods below are used to iterate through the list of clients.
     These methods should be used in a pattern similar to the following:
     
          client = clientList.firstClient();
          while(client != NULL) {
             . . .
            client = clientList.nextClient();
          }
          
      Clients should not be removed or added during the iteration over the
      clients in the container. Doing so will produce unpredictable results.  
    */
   
   
   /* Returns the first client in the iteration over the container or NULL
      if there are no clients in the container. */
  Socket *firstClient();
  
   /* Returns the next client in the iteration over the containter or NULL
      if there are no additional clients in the container. firstClient()
      must be called once to initialize the iteration over the clients. */
  Socket *nextClient();
  
  
  /*--------
     The methods below are used to associate data with a given client that
     can be accessed and used by the server as needed. These methods are
     provided for servers that need to keep additional information about
     each client connection. Typically, a struct is used to define the
     information that is needed for each client. To associate the data with
     a given connection, create a dynamic instance of the sturct using 
     malloc and pass the pointer to the addClientData method.
    ------- */
   
   /* Stores and associates data for the given client connection, based on
      the socket's file descriptor. The data to be stored must be supplied
      as a pointer. Returns true if the socket exists and no data was
      previously stored for that socket; otherwise returns false. */
  bool addData(int fd, void *data);
  
   /* Removes previously stored data for the given client connection, based
      on the socket's file descriptor. No memory is freed, the link or
      pointer to the data is simply set to NULL. Returns true if the
      connection exist and the pointer is set to NULL, returns false if the
      socket is not in the container. */
  bool removeData(int fd);
  
   /* Returns a pointer to the data previously stored for the given client
      connection. If no data was stored for the connection or the socket is
      not in the container, NULL is returned. */  
  void * getData(int fd);
  
protected:
   /* Helper method for locating the index containing the given socket.
      Returns the index if the socket is in the container and -1 otherwise. */
  int findSocket(int fd);

protected:
  int MaxConnections;
  int NumConnections;
  Socket ** TheConnections;
  void ** ClientData;
  int IterIndex;
};

#endif

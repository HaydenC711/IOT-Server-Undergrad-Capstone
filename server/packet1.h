const int HASH_SIZE = 32;
const int DEVID_SIZE = 9;  // 8 chars + \0

struct DevPacket {
  int opcode;  
              // 100 - device connecting to the server. requires the devId
  
   // used to send a parameter value with the opcode, if needed.                
  int param; 
  
   // the unique device id used when connecting.
  char devId[DEVID_SIZE]; 
  
   // needed for a full multiple of 4 sized struct.  
  //char padding[1];      
  
  //handshaking string
  char handshake[7];
};

 /* char hash[HASH_SIZE];   // the hash value that results from encrpyting the
                          // device's pass phrase and an appended sequence number.
  */             
  


const int DEV_CONN = 100;

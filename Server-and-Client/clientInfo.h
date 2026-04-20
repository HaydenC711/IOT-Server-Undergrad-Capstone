
struct ClientInfo {
  bool appConnection;   // is this an app connection or a component connection?
  bool authenticated;   // has the device authenticated?   
  int  acctNumber;      // the user account this connection is associated with
  char devId[10];
};

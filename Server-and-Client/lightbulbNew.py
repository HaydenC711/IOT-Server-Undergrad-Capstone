#!/usr/bin/python 

# This file acts as a client to the server
import socket
import sys
import struct 
#from Crypto.Hash import SHA256


DEV_CONN = 100

#Add MAC address to needed parameters
#Assume that the user running the program knows it

devId = ""
passPhrase = ""

seqNumber = 10000
clientSocket = None


def main():
  if len(sys.argv) != 3 :
    print("usage: lightbulb.py serverCompHostname severPort < devInfo")
    return
		
  host = sys.argv[1]
  port = int(sys.argv[2])
  
   # Get the device info which should have been provided via standard input
   # from information stored in a text file.
  getDeviceInfo()
  
   # Attempt to connect to the server.
  connectToServer(host, port)
	
  # Authenticate this device with the server.
  serverAuthentication()
	
	
 # The information is read from standard input, assuming it has been 
 # reidrected from a text file.			
def getDeviceInfo() :
  global devId, passPhrase
  
  devId = input() + chr(0)
  passPhrase = input()


 # Open a connection to the server, which will be left open.  
def connectToServer(host, port) :
  global clientSocket
  
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    clientSocket.connect((host, port))
    
  except:
    print("Error: could not connect to server %s on port %d." % (host, port))
    exit(1)    
  
  #Establish initial connection
  serverConnected = True
  print("Server Connected")
  
def serverAuthentication() :
	#hash = SHA256.new()
	
	
	#my code
	print("Send packet with opcode 100 and MAC address")
	
	#Send packet with opcode 100, MAC address, encrypted passphrase
	#hash.update('passPhrase')
	#hash.digest()
	packet = createPacket(DEV_CONN, handshake);
	
	
	#unpack the handshake message to ensure its correct
	storage = struct.unpack("ii9s3s", packet)
	print(storage[2].decode('ascii'))
	
	print("Sending packet with MAC address")
	clientSocket.sendall(packet)
	
	#Recieve handshaking message
	#Listen for packets being sent
	data = clientSocket.recv(60)
	print(data)
	print("len: ", len(data))
	
	storage = struct.unpack("ii9s3s", data)
	print(storage[3].decode('ascii'))
	
	
			
def createPacket(op, param=0) :
  dev = devId.encode("ascii")
  print("devId (MAC):", dev)
  print("opcode:", op)
  print(struct.calcsize('ii9s3s'));
  packet = struct.pack('ii9s3s', op, param, dev)
  print(packet)
  return packet

  
def unpackPacket(data):
	storage = struct.unpack("ii9s3s", packet)
	#print(storage[3].decode('ascii'))
	return storage
	
def encryptPassPhrase(passphrase):
	salt = Crypto.Random.get_random_bytes(SALT_SIZE)
	key = password + salt
	hashStr = hashlib.sha256(key).digest() 
	return hashStr
  			
  
  			
main()
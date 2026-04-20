#!/usr/bin/python 

# This file acts as a client to the server
import socket
import sys
from dataclasses import dataclass
from collections import namedtuple
import struct 
from typing import NamedTuple

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
	#packet = createPacket(DEV_CONN);
	#clientSocket.sendall(packet)
	
	#my code
	print("Waiting for handshaking message")
	
	#Recieve handshaking message
	#Listen for packets being sent
	data = clientSocket.recv(34)
	print(data)
	print("len: ", len(data))
	storage = struct.unpack("ii9s7s", data)
	print(storage[3].decode('ascii'))
	
	#Create handshaking response message 
	handshake = b"\rHI"
	packet = createPacket(DEV_CONN, handshake);
	
	
	#unpack the handshake message to ensure its correct
	storage = struct.unpack("ii9s7s", packet)
	print("unpacked handshake message being sent")
	print(storage[3].decode('ascii'))
	
	print("Sending handshake message")
	clientSocket.sendall(packet)
			
def createPacket(op, handshake, param=0) :
  dev = devId.encode("ascii")
  print("devId (MAC):", dev)
  print("opcode:", op)
  print(struct.calcsize('ii9s7s'));
  packet = struct.pack('ii9s7s', op, param, dev, handshake)
  print(packet)
  return packet

  
def unpackPacket(data):
	storage = struct.unpack("ii9s7s", packet)
	print("unpacked handshake message being sent")
	#print(storage[3].decode('ascii'))
	return storage
  
  			
  
  			
main()
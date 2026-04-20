#!/usr/bin/python 

# This file acts as a client to the server
import socket
import sys
import struct 

# Connect to server
DEV_CONN = 100
 
# Simple ok response, with no paramater data
DEV_OK = 101

# Response back to server with a param
DEV_REPLY = 102 

DEV_DISCONNECT = 103

# request from the server for a light bulb
DEV_LIGHT = 10000


# size of a device packet
PACKET_SIZE = 20



# ------------------
# GLOBAL VARIABLES
# ------------------

# The device id read from standard input
devId = ""

# The socket used for communicating with the server.
clientSocket = None


# Is the light currently on?
stateLightOn = False

# How long has the light been on since the last connection?
stateTimeOn = 0


def main():
  if len(sys.argv) != 3 :
    print("usage: lightbulb.py serverCompHostname dev-port < lightbulb.devId.txt")
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
  
  print("The lightbulb is currently off")
  
   # Wait for request packets from the server.
  while True :
    
    #print("Waiting for instruction...")
    packet = clientSocket.recv(PACKET_SIZE)
    #print("Packet Recieved")
    #print("Packet size: %d", len(packet))
    (opcode, param, devId) = unpackPacket(packet)
    #print("opcode:", opcode)
    #print("param:", param)
    #print("devId:", devId)
    if opcode == DEV_DISCONNECT :
    	disconnectDevice()
    elif opcode == DEV_LIGHT :
    
       # Get status of light?
      if param == 99 :
      	  #print("reporting status")
      	  reportStatus()                
        
       # Turn light on
      elif param == 1 : 
      	  changeLightState(True)
      	  
       # Turn light off
      elif param == 0 :
      	  changeLightState(False)
	
def disconnectDevice():
	packet = createPacket(DEV_DISCONNECT)
	clientSocket.sendall(packet)
	print("Disconnecting this as requested by application.")
	exit(1)
	
 # The information is read from standard input, assuming it has been 
 # reidrected from a text file.	
def getDeviceInfo() :
  global devId, salt, passPhrase
  
  devId = input()
  #Change the newline char to null character
  devId = devId[:8] + chr(0)
  
  salt = input()
  salt = salt[:len(salt)]
  #print(salt)
  
  passPhrase = input()
  passPhrase = passPhrase[:len(passPhrase)]
  #print(passPhrase)


 # Report the status of the light bulb
def reportStatus() :
  if stateLightOn :
    param = 1
  else :
    param = 0
  #print("Sending packet to the server")
  packet = createPacket(DEV_REPLY, param)
  clientSocket.sendall(packet)
  #print("IT SENT TO DEVICE.CC")
  #print("Sent packet to the server")


def changeLightState(turnOn) :
  global stateLightOn
  stateBefore = stateLightOn
   # Change the state of the light
  stateLightOn = turnOn
  if stateBefore != stateLightOn:
  	  if stateLightOn:
  	  	  print("The lightbulb is on")
  	  elif not stateLightOn:
  	  	  print("The lightbulb is off")
  	  
  
  #Do we respond with okay or the new state of light bulb?
  packet = createPacket(DEV_OK)
  clientSocket.sendall(packet)
  


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
   # Send the device id to the server to request connection.
   packet = createPacket(DEV_CONN);
   clientSocket.sendall(packet)
   # Wait for a response from the server.
   packet = clientSocket.recv(PACKET_SIZE)
   # print("Packet:", len(packet))
   (opcode, param, devId) = unpackPacket(packet)
   # See if the connection was accepted.
   if opcode == 101 :
   	   print("Connection Accepted by Server")
   elif opcode == 103:
   	   print("Error: device could not be connected. DevId isn't associated with an account.")
   	   exit(1)
	
			
def createPacket(op, param=0) :
  dev = devId.encode("ascii")
  #print(len(devId))
  #print("chr(0)", len(chr(0)))
  #print("devId (MAC):", dev)
  #print("opcode:", op)
  #print(struct.calcsize('ii9s3s'));
  padding = b"   ";
  packet = struct.pack('ii9s3s', op, param, dev, padding)
  #print(packet)
  return packet
  
def unpackPacket(packet) :
	storage = struct.unpack("ii9s3s", packet)
	opcode = int(storage[0])
	param = int(storage[1])
	devId = storage[2].decode('ascii')
	
	#print("received: %d %d %s", opcode, param, devId)
	return (opcode, param, devId)  
  			
main()
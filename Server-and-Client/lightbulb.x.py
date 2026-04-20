# This file acts as a client to the server
import socket
import sys
from dataclasses import dataclass
from collections import namedtuple
import struct 
from typing import NamedTuple

#Add MAC address to needed parameters
#Assume that the user running the program knows it

host = ""
port = 0

devId = ""
passPhrase = ""

seqNumber = 10000
clientSocket = None


def main():
	if len(sys.argv) < 3:
		print("usage: mypgm serverCompHostname severPort < devInfo")
		return
	host = sys.argv[1]
	port = int(sys.argv[2])
	connectToServer()
	#getDeviceInfo()
  

	
 # The information is read from standard input, assuming it has been 
 # reidrected from a text file.			
#def getDeviceInfo() :
 # global 
  
def connectToServer() :
	#Establish server connection
	serverConnected = False
	lightbulbOn = False
	while True:
		print(serverConnected)
		if not serverConnected:
			host = sys.argv[1]
			#print(host)
			port = int(sys.argv[2])
			MAC = sys.argv[3]
				
			#Establish initial connection
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host, port))
			serverConnected = True
			print("Server Connected")
			
			
			print("Waiting for handshaking message")
			#Recieve message and print a message if nothing recieved
			#Listen for packets being sent
			data = s.recv(34)
			print(data)
			print("len: ", len(data))
			
			#add f for float numbers
			storage = struct.unpack("ii9s7s", data)
			print(storage[3].decode('ascii'))
			
			#Create handshaking response message 
			opcode = 100
			param = 0
			devId = b""
			#padding = b""
			handshake = b"\rHI\n"
			handMessage = struct.pack('ii9s7s', opcode, param, devId, handshake)
			print(handMessage)
			
			#unpack the handshake message to ensure its correct
			storage = struct.unpack("ii9s7s", handMessage)
			print("unpacked handshake message being sent")
			print(storage[3].decode('ascii'))
			
			print("Sending handshake message")
			s.sendall(handMessage)
			
			#Send the MAC Address of the device being connected
			
			break
			
		else:
			#wait for instruction from server (use opcode)
			data = s.recv(34)
			print(data)
			print("len: ", len(data))
			
			#add f for float numbers
			storage = struct.unpack("ii9s7s", data)
			print(storage[3].decode('ascii'))
			
			opcode = storage[0]
			#if opcode == 10:
				
			
			s.close()

			
main()
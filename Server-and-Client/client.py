# This file acts as a client to the server
import socket
import sys
import struct 
import time
import getpass
import crypt
import datetime
import string
import os

# size of a device packet
PACKET_SIZE = 20

username = ""
# ------------------
# GLOBAL VARIABLES
# ------------------

# The socket used for communicating with the server.
clientSocket = None

# Is the app connected to the server?
#stateServerConnected = False

APP_INFO = 202

def main():
	if len(sys.argv) != 3 :
		print("usage: client.py serverCompHostname app-port")
		return
	host = sys.argv[1]
	port = int(sys.argv[2])
    
	# Attempt to connect to the server.
	connectToServer(host, port)
	
	loggedIn = False
	while True:
		string = False
		# login or create new user
		print("Welcome to the Main application! How would you like to proceed?")
		print()
		header = "App Options".center(20)
		try:
			response = int(input(f"{header}\n--------------------\n(1) Login \n(2) Create Account \n(3) Change Password \n(4) Quit \nSelect an option: "))
		except ValueError:
			string = True
		
		#Ensure entered value is valid
		while string == True or response not in range(1, 5):
			print("Invalid option entered!")
			try:
				response = int(input(f"{header}\n--------------------\n(1) Login \n(2) Create Account \n(3) Change Password \n(4) Quit \nSelect an option: "))
				string = False
			except ValueError:
				string = True
			
		#Execute given instruction
		if response == 1:
			loggedIn = loginUser()
			while loggedIn:
				string2 = False
				try:
					# Ask user for next step
					instruction = int(input(f"{header}\n--------------------\n(1) Add IoT device \n(2) Remove IoT device \n(3) List IoT devices \n(4) Send Device Instruction \n(5) Generate Traffic Report\n(6) Logout \nSelect an option: "))
				except ValueError:
					string2 = True
					
				# Ensure user enters a valid option
				while string2 == True or instruction not in range(1, 7):
					print("Invalid option entered! Please select from the following:")
					try:
						# Ask user for next step
						instruction = int(input("(1) Add IoT device \n(2) Remove IoT device \n(3) List IoT devices \n(4) Send Device Instruction \n(5) Generate Traffic Report\n(6) Logout \nSelect an option: "))
						string2 = False
					except ValueError:
						string2 = True
						
				#Add new device
				if instruction == 1:
					add_iot_devices()
			
				if instruction == 2:
					remove_iot_devices()
			
				#Send instruction
				elif instruction == 3:
					list_iot_devices()
			
				#List connected devices
				elif instruction == 4:
					sendInstruction()
					
				elif instruction ==5:
					generateTrafficReport()
				elif instruction == 6:
					loggedIn = False
	
		elif response == 2:
			createUser()
			loggedIn = True
		elif response == 3:
			changePass()
			loggedIn = True
		else:
			print("Closing application...")
			#send disconnect to server
			exit(1)
	


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
	print()

def changePass():
	username = input("Enter username or q to quit: ")
	result = userExists(username)
	if result != 0:
		print(f"Changing password for user {username}")
		current_password = getpass.getpass("Current Password: ")
		change_password(username, current_password, "")
	else:
		print("That username isn't in the system. Please try again.")


def userExists(username):
	# Load user account information and hashed password from the file
	if os.path.exists("user_accounts.txt"):
		with open("user_accounts.txt", "r") as file:
			for line in file:
				a = line.strip().split(":")
				if len(a) >= 3:
					if a[1] == username:
						#hashed_password = a[3]
						return a
	return 0			

def loginUser():
	global username 
	username = input("Enter username: ")
	iot_operation = '0'
	incorrect_attempts = 0
	print(f"Authenticating for user {username}")
	
	#check if username exists and set hashed password
	userInfo = userExists(username)
	if userInfo == 0:
		print("That username isn't in the system. Please try again.")
		return False
	hashed_password = userInfo[3]
	while incorrect_attempts < 3:
		input_password = getpass.getpass("Enter password: ")

		if verify_password(input_password, hashed_password):
			print("Success!! Authentication valid.\n")
			
			# Log the successful login attempt
			log_login_attempt(username, True)
			incorrect_attempts = 3
			
			#Send account Number to server so it can track application connections
			#print("Sending account number to server after successful login")
			accountNum = userInfo[0]
			packet = createPacket(APP_INFO, int(accountNum))
			clientSocket.sendall(packet)
			return True

					
		else:
			print("Error!! Authentication failed due to an invalid password.")
			log_login_attempt(username, False)
			incorrect_attempts += 1
			if incorrect_attempts == 3:
				print("Too many incorrect attempts. Shutting down...")
				print()
				return False

#I need an account number here that adds to the account struct

def createUser():
	username = input("Enter username or q to quit: ")
	
	while is_username_in_use(username) or (len(username)<=1 and username != "q") or len(username) >15:
		if len(username) <=1:
			print("Username must be more than 1 character")
		elif len(username) >=15:
			print("Username must be 15 characters or less")
		elif is_username_in_use(username):
			print("Username is already in use")
		username = input("Enter username or q to quit: ")

	if username != "q":
	
		# Read the last used userID from the existing user_accounts.txt file
		try:
			with open("user_accounts.txt", "r") as file:
				line_count = sum(1 for line in file)
				userID = line_count + 1
		except FileNotFoundError:
			userID = 1  
				
		password = getpass.getpass("Enter password: ")
		# Check if the password is strong
		while not strong_password(password):
			print("Error!! Authentication failed due to an invalid password.")
			if len(password) < 8:
				print("Password must be at least 8 characters.\n")
			if not any(char.isupper() for char in password):
				print("Password must contain at least one uppercase letter.\n")
			if not any(char.islower() for char in password):
				print("Password must contain at least one lowercase letter.\n")
			if not any(char.isdigit() for char in password):
				print("Password must contain at least one digit.\n")
			if not any(not char.isalnum() for char in password):
				print("Password must contain at least one special character.\n")
			password = getpass.getpass("Enter password: ")

		confirm_password = getpass.getpass("Confirm Password or enter q to quit: ")
		while password != confirm_password and confirm_password != "q":
			print("Password confirmation failed. Please try again.")
			# Ask the admin to confirm the password
			confirm_password = getpass.getpass("Confirm Password or enter q to quit: ")
		
		if confirm_password != "q":
			first = input("Enter first name: ")
			while not first.isalpha() or len(first) > 15 or len(first) <=1:
				if not first.strip().isalpha():
					print("First cannot include a digit or special character")
				elif len(first)>15 or len(first) <=1:
					print("First must have more than 1 character and less than 15 characters")
				first = input("Enter first name: ")
			
			last = input("Enter last name: ")
			while not last.isalpha() or len(last) > 30 or len(last) <=1:
				if not last.strip().isalpha():
					print("Last cannot include a digit or special character")
				elif len(last)>30 or len(last) <=1:
					print("Last must have more than 1 character and less than 30 characters")
				last = input("Enter last name: ")
			full_name=first + " " + last
			create_user_account(username, full_name, password, userID)

def sendInstruction():
	devices = list_iot_devices()
	if devices == 0:
		#print("There are no devices associated with this user")
		print()
	else:
		
		deviceExists = False
		print("If the device you see isn't listed please add the device info to the account with the 'Add IoT device' option")
		deviceName = input("Enter the device name of the device you would like to send an instruction to: ")
		devId = ""
		
		#Determine if the device exists
		for device in devices:
			#print(device)
			if deviceName.lower() == device[0].lower():
				devId = str(device[1])
				devId = str(devId)
				deviceExists = True
				
		while deviceExists == False:
			print("That name isn't assocated with a device.")
			deviceName = input("Enter the device name of the device you would like to send an instruction to: ")
			
			#Determine if the device exists
			for device in devices:
				if deviceName.lower() == device[0].lower():
					devId = str(device[1])
					deviceExists = True
		
		while True:
			print()
			print("Available Instructions to Send".center(35))
			print("-----------------------------------")
			print("1.) Request Device Status")
			print("2.) Turn Device On")
			print("3.) Turn Device Off")
			print("4.) Disconnect Device")
			print("5.) Return to Main Menu")
			print()
			print("Before choosing an option please make sure the device app is connected!")
			print()
			answer = int(input("Please Select one of the Above options: "))
			
			#send packet to server
			
			#Query the device
			if answer == 1:
				writeTraffic(10000, 99, devId)
				queryDevice(devId)
				
			elif answer == 2:
				writeTraffic(10000, 1, devId)
				toggleDeviceStatus(1, devId)
			elif answer == 3:
				writeTraffic(10000, 0, devId)
				toggleDeviceStatus(0, devId)
			elif answer == 4:
				writeTraffic(103,"N/A", devId)
				disconnectDev(devId)
			elif answer == 5:
				print()
				return
			else:
				print("Invalid Option! Please try again.")
				print()

def disconnectDev(devId):
	packet = createPacket(103, -1, devId)
	
	clientSocket.sendall(packet)
	print("Device Disconnected")
	print()

def toggleDeviceStatus(desiredState, device):
	currentStatus = queryDevice(device)
	if currentStatus != desiredState:
		#Send packet to device with correct opcode
		packet = createPacket(10000, desiredState, device)
		clientSocket.sendall(packet)
		
		#receive the packet
		print("Sending to server")
		(opcode, param, devId) = receivePacket()
		#send packet to device
		#print(opcode)
		if opcode == 101:
			print("Device status successfully toggled")
			return True
	elif currentStatus == 0:
		print("Device is already off")
	elif currentStatus == 1:
		print("Device is already on")
	return False
		
	
	
def queryDevice(device):
	#Send packet to device with correct opcode
	packet = createPacket(10000, 99, device)
	clientSocket.sendall(packet)
		
	#receive the packet
	try:
		(opcode, param, devId) = receivePacket()
		if param == 0:
			print("The device is turned off")
		elif param == 1:
			print("The device is turned on")
		else:
			print("The device state is unknown")
			print("Please connect the device application!")
		return param
	except TypeError:
		print("Please make sure the device application is connected!")
		return -1
	

def receivePacket():
	try:
		packet = clientSocket.recv(PACKET_SIZE)
		#print("Packet Recieved")
		#print("Packet size: %d", len(packet))
		(opcode, param, devId) = unpackPacket(packet)
		writeTraffic(opcode, param, devId, "Reply")
		return (opcode, param, devId)
	except TypeError:
		print("Please make sure the device application is connected!")
	
	
def writeTraffic(opcode, param, devId, message="Instruction"):
	#Read traffic number and create date
	lines = []
	if os.path.exists(f"traffic.{username}.txt"):
		with open(f"traffic.{username}.txt", "r") as traffic_txt:
			for line in traffic_txt:
				lines.append(line.strip())
			lines2 = lines[-1].split('|')
			lines3 = lines2[0].split(':')
		if message =="Instruction":
			traffic_no=int(lines3[1])+10
		elif message == "Reply":
			traffic_no=int(lines3[1])
	else:
		traffic_no = 1000
	# Get the current date and time
	current_datetime = datetime.datetime.now()
	# Format the date and time
	formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
	
	# Getting IP address of the user
	host_name = socket.gethostname()
	ip_address = socket.gethostbyname(host_name)
	explanation = ""
	if opcode == 103:
		explanation = "Disconnect Device"
	elif opcode == 10000:
		if param == 0:
			explanation = "Turn lightbulb off"
		elif param == 1:
			explanation = "Turn lightbulb on"
		elif param == 99:
			explanation = "Query lightbulb status"
	#DEV_REPLY for query
	elif opcode == 102:
		if param == 1:
			explanation = "The lightbulb is on"
		elif param == 0:
			explanation = "The lightbulb is off"
	#DEV_OK
	elif opcode == 101:
		explanation = "OK"
			
	with open(f"traffic.{username}.txt", "a") as traffic_file:
		traffic_file.write(f"Traffic Number:{traffic_no}|Date/Time:{formatted_datetime}|Device ID:{devId}|Opcode:{opcode}|Parameter:{param}|Message Type:{message}|Explanation:{explanation}|Source IP:{ip_address}\n")
		
def generateTrafficReport():
	if os.path.exists(f"traffic.{username}.txt"):
		with open(f"traffic.{username}.txt", "r") as traffic_txt:
			for line in traffic_txt:
				print(line)
	else:
		print("No traffic to report.")


def add_iot_devices():
	b = 1
	print(f"\nLogged in as user {username}")
	
	while b == 1:
		
		device_name = input("\nEnter the name of the IoT device or 'q' to quit: ")
		
		
		
		if device_name.lower() != 'q':
			
			#Check if the file exists (iotList.txt)
			deviceNameExists = False
			if os.path.exists('iotList.txt'):
				devices = getDevices()
				for device in devices:
					#print(device)
					if device_name.lower() == device[0].lower():
						deviceNameExists = True
			
			while deviceNameExists or len(device_name) <= 1 or len(device_name) > 15:
				if deviceNameExists:
					print("That device name already exists. Please try again")
					device_name = input("\nEnter the name of the IoT device or 'q' to quit: ")
					deviceStillExists = False
					for device in devices:
						if device_name.lower() == device[0].lower():
							deviceStillExists = True
					if not deviceStillExists:
						deviceNameExists = False
				elif len(device_name) <= 1:
					print("Device name length must be greater than 1 character. Please try again!")
					device_name = input("\nEnter the name of the IoT device or 'q' to quit: ")
				elif len(device_name) > 15:
					print("Device name must be less than 15 characters. Please try again")
					device_name = input("\nEnter the name of the IoT device or 'q' to quit: ")

			
			device_id = input("\nEnter the device ID of the IoT device: ")
			
			
			
			devCodes = ["LT", "DL", "CM"]
			specialChar = False
			
			for i in range(0, len(device_id)):
					if device_id[i] in string.punctuation:
						specialChar = True
			
			while len(device_id) != 8 or device_id[:2] not in devCodes or specialChar or device_id.isdigit() or device_id.isalpha() or checkDevId(device_id):
				if checkDevId(device_id):
					print("Device already exists")
				elif len(device_id) != 8:
					print("Device ID must be 8 characters")
				
				elif specialChar == True:
					print("Device ID cannot contain special characters")
					specialChar = False
				elif device_id.isdigit():
					print("Device ID cannot be a number")
				elif device_id.isalpha():
					print("Device ID must contain a number")
				else:
					print("Device ID must start with 'LT', 'DL', or 'CM'. (LT for Lightbulb, DL for Doorlock, CM for Camera")
				device_id = input("\nEnter the device ID of the IoT device: ")
				
				for j in range(0, len(device_id)):
					if device_id[j] in string.punctuation:
						specialChar = True
			
			passphrase = str(input("Enter passphrase: "))
			while len(passphrase) > 35 or len(passphrase) <= 1:
				if len(passphrase) > 35:
					print("The passphrase must be less than 35 characters!")
				elif len(passphrase) <= 1:
					print("The passphrase must be greater than 1 character")
				passphrase = str(input("Enter passphrase: "))
				#passphrase = getpass.getpass("Enter Passphrase: ")
			salt = crypt.mksalt(crypt.METHOD_SHA512)
			#print(salt)
			hashed= crypt.crypt(passphrase, salt)
			#print(device_id[:2])
			
			if device_id[:2] == "LT":
				devType = "lightbulb"
			elif device_id[:2] == "DL":
				devType = "doorlock"
			elif device_id[:2] == "CM":
				devType = "camera"
			
			# Append the device information with MAC address to a file
			with open("iot_devices.txt", "a") as iot_file:
				iot_file.write(f"{username}\n")
				iot_file.write(f"{device_name}\n")
				iot_file.write(f"{device_id}\n")
				iot_file.write(f"{salt}\n")
				iot_file.write(f"{passphrase}\n")
			
			with open(f"{devType}.{device_id}.txt", "w") as device_file:
				device_file.write(f"{device_id}\n")
				device_file.write(f"{salt}\n")
				device_file.write(f"{passphrase}\n")
			
			with open("iotList.txt", "a") as list_file:
				list_file.write(f"User: {username}, IoT Device: {device_name}, device_id: {device_id}\n")
			print(f"\nDevice {device_name} with device id {device_id} was added.")
			
			packet = createPacket(203, 1, device)
			clientSocket.sendall(packet)
			
		else:
			#print("Done\n")
			b = 0
	print("")

def createPacket(op, param=-1, devId="") :
  dev = devId.encode('ascii')
  #print(dev)
  #print("devId (MAC):", devId)
  #print("opcode:", op)
  #print(struct.calcsize('ii9s3s'));
  padding = b"   "
  #print(padding)
  packet = struct.pack('ii9s3s', op, param, dev, padding)
  #print(packet)
  return packet
  
def unpackPacket(packet) :
	try:
		storage = struct.unpack("ii9s3s", packet)
		opcode = int(storage[0])
		param = int(storage[1])
		devId = storage[2].decode('ascii')
		
		#print("received: %d %d %s", opcode, param, devId)
		return (opcode, param, devId)  
	except struct.error:
		print("Please make sure the device application is connected!")
	
# Function to check if a password meets the password policy
def strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(not char.isalnum() for char in password):
        return False
    return True

# Function to verify a password against a stored hashed password
def verify_password(input_password, stored_password):
    return crypt.crypt(input_password, stored_password) == stored_password
    
# Function to check if a username is already in use
def is_username_in_use(username):
	if os.path.exists("user_accounts.txt"):
		with open("user_accounts.txt", "r") as file:
			for line in file:
				partof = line.strip().split(":")
				if len(partof) >= 2 and partof[1] == username:
					return True
	return False

# Function to create a new user account
def create_user_account(username, full_name, password, userID):
    # Check if the username is already in use
    if is_username_in_use(username):
        print("Error!! Username is already in use.\n")
        return False
        
    # Collect additional user information
    home_address = input("Enter home address: ")
    phone_number = input("Enter phone number: ")
    email_address = input("Enter email address: ")

    # Generate a random salt using crypt.mksalt
    salt = crypt.mksalt(crypt.METHOD_SHA512)

    # Hash the password with the salt
    hashed_password = crypt.crypt(password, salt)

    # Store the user account information and hashed password in a file
    with open("user_accounts.txt", "a") as account_file:
        account_file.write(f"{userID}:{username}:{salt}:{hashed_password}\n")
        
    # Store the additional user details in a separate file
    with open("user_details.txt", "a") as details_file:
        details_file.write(f"{userID}\n")
        details_file.write(f"{username}\n")
        details_file.write(f"{full_name}\n")
        details_file.write(f"{home_address}\n")
        details_file.write(f"{phone_number}\n")
        details_file.write(f"{email_address}\n")

    print("User account created successfully!!")
    return True
    
# Function to change a user's password
def change_password(username, current_password, new_password):
    # Load user account information and hashed password from the file
    with open("user_accounts.txt", "r") as account_file:
        lines = account_file.readlines()

    updated_lines = []
    b = 1

    for line in lines:
        a = line.strip().split(":")
        if len(a) >= 4: 
            if a[1] == username:
                userID = a[0]
                salt = a[2]
                hashed_password = a[3]
                if verify_password(current_password, hashed_password):
                    while b == 1:
                        new_password = getpass.getpass("New Password: ")
                        if strong_password(new_password):
                            new_password2 = getpass.getpass("Re-enter new password: ")
                            if new_password == new_password2:
                                # Generate a new random salt using crypt.mksalt
                                new_salt = crypt.mksalt(crypt.METHOD_SHA512)
        
                                # Cryptographically hash the new password with the new salt
                                new_hashed_password = crypt.crypt(new_password, new_salt)
        
                                updated_line = f"{userID}:{username}:{new_salt}:{new_hashed_password}\n"
                                updated_lines.append(updated_line)
                                print("Password changed successfully.")
                                b = 0
                                
                                # Update the password in the file
                                with open("user_accounts.txt", "w") as update_file:
                                    update_file.writelines(updated_lines)
                                    
                            else:
                                print("Error!! Authentication failed due to passwords not matching.")
                        else:
                            print("Error!! Authentication failed due to an invalid password.\nPassword must be at least 8 characters long.\nPassword must contain upper- and lower-case letters.\nPassword must contain a number.\nPassword must contain a non-alphanumeric character.")
                else:
                    print("Error!! Authentication failed due to an invalid current password.")
            else:
                updated_lines.append(line)


# Function to remove IoT devices from a user's account
def remove_iot_devices():
    h = 1
    print(f"Logged in as user {username}")
    
    device_info = []
    with open("iot_devices.txt", "r") as iot_info:
    	for line in iot_info:
    		device_info.append(line.strip())
    
    devices = []
    with open("iotList.txt", "r") as iot_file:
        for line in iot_file:
            if f"{username}" in line:
                devices.append(line)

    if not devices:
        print("No devices found for this user.")
        return 0

    print("Devices associated with this user:")
    for i, device in enumerate(devices):
        print(f"{i + 1}: {device.strip()}")

    while h == 1:
    	# try:
    	choice = (input("Enter the number of the device to remove, or 'q' to quit: "))
    	if not choice.isdigit():
    		if choice == "q":
    			h = 0
    		else:
    			print("Invalid entry. Please enter the number of the device to be removed!")
    			print()
    	elif 1 <= int(choice) <= len(devices):
    		choice2 = (input("Enter the number of the device to confirm, or 'q' to quit: "))
    		if not choice2.isdigit():
    			if choice2 == "q":
    				h = 0
    			else:
    				print("Invalid entry. Please enter the number of the device to be removed!")
    				print()
    		elif int(choice2) == int(choice):
    			choice = int(choice)
    			temp = devices[int(choice)-1].split(",")
    			device_id = temp[2][12:]
    			ndx= 0
    			for i in range(0, len(device_info)):
    				if device_info[i] == device_id.strip():
    					ndx = i
    			#print("ndx", ndx)
    			device_info.pop(ndx+2)
    			device_info.pop(ndx+1)
    			device_info.pop(ndx-2)
    			device_info.pop(ndx-2)
    			device_info.pop(ndx-2)
    			removed_device = devices.pop(choice - 1)
    			with open("iotList.txt", "w") as iot_file:
    				iot_file.writelines(devices)
    			with open("iot_devices.txt", "w") as iot_info:
    				for i in range(0, len(device_info)):
    					iot_info.write(device_info[i])
    					iot_info.write("\n")
    			print(f"Removed device: {removed_device.strip()}")
    		else:
    			print("Digit Entered isn't the same as the previous. Please try again")
    		
    	else:
    		print("Invalid choice. Please select a valid device or 'q' to quit.")
    	'''except ValueError:
    		if input("Enter 'q' to quit or anything else to continue: ").lower() == 'q':
        		h = 0'''

    

# Function to list IoT devices for a user
def list_iot_devices():
	devices = []
	if os.path.exists('iotList.txt'):
		devices = getDevices()
		if len(devices) > 0:
			print(f"\nIoT devices associated with user {username}:")
			for device in devices:
			   print("Device Name: %s, Device ID: %s" % (device[0], device[1]))
			print()
			return devices
	print()
	print(f"No IoT devices found for user {username}.")
	print()
	return 0
			
            
def getDevices():
	with open("iotList.txt", "r") as iot_file:
		devices = []
		
		for line in iot_file:
			temp2 = []
			temp4 = []
			if f"{username}" in line:
				temp = line.split(',')
				
				for i in range(1, len(temp)):
					temp2.append(temp[i])
				for j in range(0, len(temp2)):
					temp3 = []
					temp3 = temp2[j].split(':')
					temp4.append(temp3[1].strip())
					
				devices.append(temp4)
		return devices

def devIdList():
	with open("iotList.txt", "r") as iot_file:
		devices = []
		devIdList = []
		
		for line in iot_file:
			temp2 = []
			temp4 = []

			temp = line.split(',')
					
			for i in range(1, len(temp)):
				temp2.append(temp[i])
			
			
			for j in range(0, len(temp2)):
				temp3 = []
				temp3 = temp2[j].split(':')
				temp4.append(temp3[1].strip())
				
			devices.append(temp4)
		
		#print("Length Devices", len(devices))
		#print(devices)
		
		for device in devices:
			if len(device) != 0:
				devIdList.append(device[1])
		#print("devIdList: ", devIdList)
		return devIdList

def checkDevId(devId):
	if os.path.exists('iotList.txt'):
		devIds = devIdList()
		for ID in devIds:
			print("ID: ", ID)
			if devId.lower() == ID.lower():
				return True
	return False
# Function to log login attempts
def log_login_attempt(username, success, ip_address=None):
    if success:
        try:
            # Get the current date and time
            current_datetime = datetime.datetime.now()
            # Format the date and time
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            # Getting IP address of the user
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            
            # Log the date and time of the last successful login
            with open("login_logs.txt", "a") as log_file:
                log_file.write(f"User {username} logged in successfully at {formatted_datetime} from IP address {ip_address}\n")
        except socket.gaierror:
            print("Error: Unable to retrieve the IP address")
    else:
        try:
            # Get the current date and time
            current_datetime = datetime.datetime.now()
            # Format the date and time
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # Getting IP address of the user
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            
            # Log the date and time of the last successful login
            with open("login_logs.txt", "a") as log_file:
                log_file.write(f"User {username} failed login at {formatted_datetime} from IP address {ip_address}\n")
        except socket.gaierror:
            print("Error: Unable to retrieve the IP address")
            
def addDevtoFile(devId):
	#Add device data to the device struct
	#generate salt and passphrase
	salt = crypt.mksalt(crypt.METHOD_SHA512)
	passphrase = input("Enter a passphrase for the device of up to 35 letters. This will be used in the authentication process and you don't have to remember it: ")
				
	#Add the device informaton to corresponding files
		#Do I add the device to the lightbulb.1.txt file?   Dev Id is and passphrase is stored into the next 
		#How would the lightbulb know which line to pull data from? data is hardcoded into lightbulb 
		#Separate files for each account or stored in struct?
		#in devices.cc, the devStruct with info from the txt file so that would have to get re worked
			
main()

#application behavior

#If outside entry is detected 
	#Send packet to server containing an opcode and attack info
	
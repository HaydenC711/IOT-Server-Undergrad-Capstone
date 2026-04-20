'''def loginUser():
	username = input("Enter username: ")
	iot_operation = '0'
	incorrect_attempts = 0
	print(f"Authenticating for user {username}")
	while incorrect_attempts < 3:
		input_password = getpass.getpass("Enter password: ")
		# Load user account information and hashed password from the file
		with open("user_accounts.txt", "r") as file:
			for line in file:
				a = line.strip().split(":")
				if len(a) >= 3:
					if a[1] == username:
						hashed_password = a[3]
						
						
						
						if verify_password(input_password, hashed_password):
							print("Success!! Authentication valid.\n")
							
							# Log the successful login attempt
							log_login_attempt(username, True)
							incorrect_attempts = 3
							
							#Send account Number to server so it can track application connections
							print("Sending account number to server after successful login")
							accountNum = a[0]
							packet = createPacket(APP_INFO, int(accountNum))
							clientSocket.sendall(packet)
							return True
							
							
									
						else:
							print("Error!! Authentication failed due to an invalid password.")
							log_login_attempt(username, False)
							incorrect_attempts += 1
							if incorrect_attempts == 3:
								print("Too many incorrect attempts. Shutting down...")
								return False'''
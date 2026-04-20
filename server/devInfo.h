
struct Device {
	char[10] devType; 
	char[8] devId;       //Device Id that server recieves while connecting with device
	char[36] passphrase; //35 chars + \0: passphrase entered by user when adding device to account from main app
	int saltValie;        // salt value generated when user adds device from main app
}
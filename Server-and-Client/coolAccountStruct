/*struct Device {
	char username[50];
	char[15] devType; 
	char[8] devId;       //Device Id that server recieves while connecting with device
	char[36] passphrase; //35 chars + \0: passphrase entered by user when adding device to account from main app
	int saltValue;        // salt value generated when user adds device from main app
};

// Define a struct for user details
struct UserDetails {
    int userID;
    char username[50];
    char full_name[50];
    char home_address[50];
    int phone_num;
    char email;
    struct* Devices;
};


#Fill Account data


	#add to list of account structs

#fill device
	#for user
		#find acount struct
			#fill out device struct
			#add passphrases (function?)
			
			#add it into devices struct in account struct
			
	

#add passphrase */

#include <stdio.h>

#define MAX_USERS 10
#define MAX_DEVICES 10

struct Device {
    char type[10];
    char devId[9];
    char passphrase[36];
    int saltValue;
};

struct UserDetails {
    int userID;
    char username[50];
    char full_name[50];
    char home_address[50];
    int phone_num;
    char email[50];
    Device devices[MAX_DEVICES];
    int numDevices;
};

UserDetails users[MAX_USERS];
int numUsers = 0;

void addDevice(struct Device newDevice) { //struct UserDetails *user, struct Device newDevice
    if (users->numDevices < MAX_DEVICES) {
        users->devices[users->numDevices] = newDevice;
        users->numDevices++;
    }
}

void readDeviceData(struct Device devices[], int *numDevices) {
    FILE *file = fopen("iot_devices.txt", "r");
    if (file == NULL) {
        printf("Error opening device file.\n");
        return;
    }
    char username[50];
    while (fscanf(file, "%s %s %s %s %d",
                  username,    //username isnt stored in the devices struct
                  devices[*numDevices].type,
                  devices[*numDevices].devId,
                  devices[*numDevices].passphrase,
                  &devices[*numDevices].saltValue) == 5) {

        (*numDevices)++;
        
        //We can remove this if statement because this would be handled when clients are made on the main app
        if (*numDevices >= MAX_DEVICES) {
            break;
        }
    }

    fclose(file);
}

void readUserData() { //struct UserDetails users[], int *numUsers
    FILE *file = fopen("user_details.txt", "r");
    if (file == NULL) {
        printf("Error opening user file.\n");
        return;
    }
    printf("Hi2\n");
    struct Device devices[MAX_DEVICES];
    printf("Hi3\n");
    int numDevices = 0;

    while (fscanf(file, "%d %s %s %s %d %s",
                  users[numUsers].userID, //&users
                  users[numUsers].username,
                  users[numUsers].full_name,
                  users[numUsers].home_address,
                  users[numUsers].phone_num, //&users
                  users[numUsers].email) == 6) { 
    	printf("Hi4\n");
        readDeviceData(devices, &numDevices);
        printf("Hi5\n");
        for (int i = 0; i < numDevices; i++) {
            addDevice(devices[i]);
        }

        (numUsers)++;
        if (numUsers >= MAX_USERS) {
            printf("To many users");
        }
    }

    fclose(file);
}

/**void printUserDetails(){
	printf("%d\n", sizeof(users));
	
	int i = 0;
	//while (i< numUsers){
		//printf("%s\n", users[i].username);	
		
	//}
}**/

int main() {

	printf("Hi1\n");
    readUserData();      //users, &numUsers
    for (int i = 0; i < numUsers; i++) {
    	printf("Hi\n");
    	printf("User ID: %d\n", users[i].userID);
    	printf("Username: %s\n", users[i].username);
    	printf("Devices:\n");

    	for (int j = 0; j < users[i].numDevices; j++) {
    		printf("   Device Type: %s\n", users[i].devices[j].type);
    		printf("   Device ID: %s\n", users[i].devices[j].devId);
    	}
    	printf("\n");
    }	
    
   // printUserDetails();
}



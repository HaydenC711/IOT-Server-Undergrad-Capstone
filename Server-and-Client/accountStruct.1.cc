/* accountStruct.cc */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 100

// Define a struct for IoT information
struct IoTInfo {
	char type[10];
    char device[50];
    char devId[9];
};

// Define a struct for user details
struct UserDetails {
    int userID;
    char username[50];
    IoTInfo devices[10];
};



//Define list of accounts and list of devices
UserDetails users[MAX_USERS]; 

int main() {
    // Read user details from user_details.txt and store them in an array
    int numUsers = 0;

    FILE *userDetailsFile = fopen("user_details.txt", "r");
    if (userDetailsFile != NULL) {
        char line[256];
        while (numUsers < MAX_USERS && fgets(line, sizeof(line), userDetailsFile) != NULL) {         //fgets doesn't return null
            sscanf(line, "%d : %49s", &users[numUsers].userID, users[numUsers].username);
            ++numUsers;
            
            printf("%s\n", line);
            
            //Add account to list of accounts
            
        }
        fclose(userDetailsFile);
    } else {
        fprintf(stderr, "Unable to open user_details.txt\n");
        return 1;
    }

    // Read IoT information from iot_devices.txt
    struct IoTInfo iotInfo[MAX_USERS];
    int numIoTInfo = 0;  // Counter for IoT information

    FILE *iotDevicesFile = fopen("iot_devices.txt", "r");
    if (iotDevicesFile != NULL) {
        char line[256];
        while (numIoTInfo < MAX_USERS && fgets(line, sizeof(line), iotDevicesFile) != NULL) {
            char username[50];
            int deviceID; 
            // Adjust the format specifier to match the format in the file
            sscanf(line, "User: %s, IoT Device: %s, device_id: %d",
                   username, iotInfo[numIoTInfo].device, &deviceID);

            
            // Find the corresponding user in the users array
            for (int i = 0; i < numUsers; ++i) {
                if (strcmp(username, users[i].username) == 0) {
                    // Assign the user ID to the IoTInfo struct
                    iotInfo[numIoTInfo].deviceID = deviceID;
                    strcpy(iotInfo[numIoTInfo].username, username);
                }
            }
            ++numIoTInfo;
        }
        fclose(iotDevicesFile);
    } else {
        fprintf(stderr, "Unable to open iot_devices.txt\n");
        return 1;
    }

    // Process the collected information as needed
    for (int i = 0; i < numUsers; i++) {
        // Find the corresponding IoT information for each user
        int j;
        for (j = 0; j < numIoTInfo; j++) {
        	printf("numIot: %d\n", numIoTInfo);
        	printf("j: %d\n", j);
            if (strcmp(users[i].username, iotInfo[j].username) == 0) {
            }
        }

        // Print user details and IoT information for each user
        printf("User Details: %d %s\n", users[i].userID, users[i].username);
        if (j < numIoTInfo) {
            printf("IoT Info: %s %s %d\n", iotInfo[j].username, iotInfo[j].device, iotInfo[j].deviceID);
        } else {
            printf("IoT Info: No information available\n");
        }
    }
}

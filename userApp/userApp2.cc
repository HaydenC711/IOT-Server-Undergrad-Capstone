#include <stdio.h>
#include <stdlib.h>
#include <ctime>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <crypt.h>
#include <string>

bool isStrongPassword(const char* password);
bool verifyPassword(const char* inputPassword, const char* storedPassword);
bool isUsernameInUse(const char* username);
void createUserAccount(const char* username, const char* fullName, const char* password, int& userID);
void changePassword(const char* username, const char* currentPassword, const char* newPassword);
void addIoTDevices(const char* username);
void removeIoTDevices(const char* username);

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Error: Missing command-line arguments.\n");
        return 1;
    }

    const char* operation = argv[1];
    const char* username = argv[2];

    if (strcmp(operation, "c") == 0) {
        printf("Changing password for user %s\n", username);
        // Changing password
        char currentPassword[256];
        printf("Current Password: ");
        scanf("%s", currentPassword);
        changePassword(username, currentPassword, "");

  } else if (strcmp(operation, "a") == 0) {
    	// Authenticating user
        printf("Authenticating for user %s\n", username);

        int incorrectAttempts = 0;
        while (incorrectAttempts < 3) {
            char enteredPassword[256];
            printf("Enter password for authentication: ");
            scanf("%s", enteredPassword);

            if (authenticateUser(username, enteredPassword)) {
                printf("Success!! Authentication valid.\n");

                char iot = 'a';
                while (iot != 'q') {
                    printf("(1) Add IoT device\n(2) Remove IoT device\n(3) List IoT devices\n(q) Quit\nSelect: ");
                    scanf(" %c", &iot);

                    if (iot == '1') {
                        addIoTDevices(username);
                    } else if (iot == '2') {
                        removeIoTDevices(username);
                    } else if (iot == '3') {
                        // Add logic for listing IoT devices
                    }
                }

                // Log the successful login attempt
                // logLoginAttempt(username, true);
                break;
            } else {
                printf("Error!! Authentication failed due to an invalid password.\n");
                // logLoginAttempt(username, false);
                incorrectAttempts++;
                if (incorrectAttempts == 3) {
                    printf("Too many incorrect attempts. Shutting down...\n");
                }
            }
        }
    } else if (strcmp(operation, "n") == 0) {
        printf("Creating a new account for user %s\n", username);
        
        char password[256];
        printf("Enter password for the new account: ");
        scanf("%s", password);
        createUserAccount(username, full_name, password, userID);
    
    } else {
        fprintf(stderr, "Error: Invalid operation. Use 'c' to change password, 'a' to authenticate, or 'n' to create a new account.\n");
        return 1;
    }

    return 0;
}

bool isStrongPassword(const char* password) {
    int length = strlen(password);
    return (length >= 8 &&
            strpbrk(password, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") != NULL &&
            strpbrk(password, "abcdefghijklmnopqrstuvwxyz") != NULL &&
            strpbrk(password, "0123456789") != NULL &&
            strpbrk(password, "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~") != NULL);
}

bool verifyPassword(const char* inputPassword, const char* storedPassword) {
    return crypt(inputPassword, storedPassword) == storedPassword;
}

bool isUsernameInUse(const char* username) {
    FILE* file = fopen("user_accounts.txt", "r");
    if (file != NULL) {
        char line[256];
        while (fgets(line, sizeof(line), file) != NULL) {
            char* partof = strtok(line, ":");
            if (partof != NULL && strcmp(partof, username) == 0) {
                fclose(file);
                return true;
            }
        }
        fclose(file);
    }
    return false;
}

void createUserAccount(const char* username, const char* fullName, const char* password, int& userID) {
    char salt[256];
    sprintf(salt, "$6$%ld$", time(NULL));

    char hashedPassword[256];
    strcpy(hashedPassword, crypt(password, salt));

    FILE* file = fopen("user_accounts.txt", "a");
    if (file != NULL) {
        fprintf(file, "%d:%s:%s:%s:%s\n", userID, username, fullName, salt, hashedPassword);
        fclose(file);
    }

    printf("User account created successfully!!\n");

    try {
        FILE* file = fopen("user_accounts.txt", "r");
        if (file != NULL) {
            int lineCount = 0;
            char line[256];
            while (fgets(line, sizeof(line), file) != NULL) {
                lineCount++;
            }
            fclose(file);
            userID = lineCount + 1;
        }
    } catch (...) {
        userID = 1;
    }
}

void changePassword(const char* username, const char* currentPassword, const char* newPassword) {
    FILE* file = fopen("user_accounts.txt", "r");
    if (file != NULL) {
        char line[256];
        char lines[100][256];
        int lineCount = 0;

        while (fgets(line, sizeof(line), file) != NULL) {
            strcpy(lines[lineCount], line);
            lineCount++;
        }
        fclose(file);

        char updatedLines[100][256];
        int b = 1;

        for (int i = 0; i < lineCount; i++) {
            char* token = strtok(lines[i], ":");
            char* parts[5];
            int partCount = 0;
            while (token != NULL) {
                parts[partCount++] = token;
                token = strtok(NULL, ":");
            }

            if (partCount >= 5) {
                if (strcmp(parts[1], username) == 0) {
                    int userID = atoi(parts[0]);
                    const char* salt = parts[3];
                    const char* hashedPassword = parts[4];

                    if (verifyPassword(currentPassword, hashedPassword)) {
                        while (b == 1) {
                            char newPassword[256];
                            printf("New Password: ");
                            scanf("%s", newPassword);

                            if (isStrongPassword(newPassword)) {
                                char newPassword2[256];
                                printf("Re-enter new password: ");
                                scanf("%s", newPassword2);

                                if (strcmp(newPassword, newPassword2) == 0) {
                                    char newSalt[256];
                                    sprintf(newSalt, "$6$%ld$", time(NULL));

                                    char newHashedPassword[256];
                                    strcpy(newHashedPassword, crypt(newPassword, newSalt));

                                    sprintf(updatedLines[i], "%d:%s:%s:%s:%s\n", userID, username, parts[2], newSalt, newHashedPassword);

                                    printf("Password changed successfully.\n");
                                    b = 0;

                                    FILE* updateFile = fopen("user_accounts.txt", "w");
                                    if (updateFile != NULL) {
                                        for (int j = 0; j < lineCount; j++) {
                                            fprintf(updateFile, "%s", updatedLines[j]);
                                        }
                                        fclose(updateFile);
                                    }

                                } else {
                                    printf("Error!! Authentication failed due to passwords not matching.\n");
                                }
                            } else {
                                printf("Error!! Authentication failed due to an invalid password."
                                       "\nPassword must be at least 8 characters long."
                                       "\nPassword must contain upper- and lower-case letters."
                                       "\nPassword must contain a number."
                                       "\nPassword must contain a non-alphanumeric character.\n");
                            }
                        }
                    } else {
                        printf("Error!! Authentication failed due to an invalid current password.\n");
                    }
                } else {
                    strcpy(updatedLines[i], lines[i]);
                }
            }
        }
    }
}

void addIoTDevices(const char* username) {
    int b = 1;
    printf("Logged in as user %s\n", username);

    while (b == 1) {
        char deviceName[256];
        printf("\nEnter the name of the IoT device or 'q' to quit: ");
        scanf("%s", deviceName);

        if (strcmp(deviceName, "q") != 0) {
            FILE* iotFile = fopen("iot_devices.txt", "a");
            if (iotFile != NULL) {
                fprintf(iotFile, "User: %s, IoT Device: %s\n", username, deviceName);
                fclose(iotFile);
                printf("Device %s was added.\n", deviceName);
            }
        } else {
            printf("Done\n");
            b = 0;
        }
    }
    printf("\n");
}

void removeIoTDevices(const char* username) {
    int h = 1;
    printf("Logged in as user %s\n", username);
    char devices[100][256];
    int deviceCount = 0;  
    FILE* iotFile = fopen("iot_devices.txt", "r");
    if (iotFile != NULL) {
        char line[256];
        while (fgets(line, sizeof(line), iotFile) != NULL) {
            const char* userString = "User: ";
            const char* usernameString = username;
            if (strstr(line, userString) != NULL && strstr(line, usernameString) != NULL) {
                strcpy(devices[deviceCount], line);
                deviceCount++;
            }
        }
        fclose(iotFile);
    }

    if (deviceCount > 0) {
        printf("Devices associated with this user:\n");
        for (int i = 0; i < deviceCount; i++) {
            printf("%d: %s", i + 1, devices[i]);
        }

        while (h == 1) {
            int choice;
            printf("Enter the number of the device to remove, or 0 to quit: ");
            scanf("%d", &choice);

            if (choice >= 1 && choice <= deviceCount) {
                // Remove the selected device
                FILE* iotFile = fopen("iot_devices.txt", "w");
                if (iotFile != NULL) {
                    for (int i = 0; i < deviceCount; i++) {
                        if (i != choice - 1) {
                            fprintf(iotFile, "%s", devices[i]);
                        }
                    }
                    fclose(iotFile);
                    printf("Device removed successfully.\n");
                    h = 0;
                }
            } else if (choice == 0) {
                printf("Done\n");
                h = 0;
            } else {
                printf("Invalid choice. Please enter a valid device number or 0 to quit.\n");
            }
        }
    } else {
        printf("No devices associated with this user.\n");
    }
}

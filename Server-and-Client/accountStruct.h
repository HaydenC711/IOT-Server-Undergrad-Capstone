#ifndef _ACCOUNTSTRUCT_H
#define _ACCOUNTSTRUCT_H
#define MAX_USERS 10
#define MAX_DEVICES 10

#include "clientInfo.h"
#include "connections.h"

struct Device {
    char type[16];
    char devId[9];
    char salt[21];
    char passphrase[36];
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


//Code for acocunt struct



//Function Prototypes
int readDeviceData(struct Device devices[], char username[50]);
void readUserData();
//void loadDevices();
//Connections getDevList();

 /* Go through the list of attached devices and get the fd's for each
    device that belongs to the given account. Returns the number of 
    connected devices for the given account. */
//int getUsersDevices(int acctNum, int fdList[]);

int findAccountNum(char* devId);
void clearData();

int getNumUsers();
UserDetails *getUsers();
int checkDevId(char* devId);



#endif
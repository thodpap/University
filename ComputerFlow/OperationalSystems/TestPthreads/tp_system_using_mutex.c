#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

struct account {
	char name[20];
	int balance;
};

//Globally shared account details
struct account yac = {"badboy", 100};

//Lock to be used while updating account balance
pthread_mutex_t lock;

void* deposit(void* data) {
	int ammount = *((int*)data);
//	pthread_mutex_lock(&lock);
	printf("Account Holder: %s, Current balance: Rs. %d\n", yac.name, yac.balance);

	printf("Depositing Rs. %d…\n", ammount);
	pthread_mutex_lock(&lock);
	yac.balance += ammount;
	pthread_mutex_unlock(&lock);

	printf("Account Holder: %s, Updated balance: Rs. %d\n\n", yac.name, yac.balance);

	return (void*)NULL;
}

int main(int argc, char** argv) {
	int i, n;
	n = 2; //Increase value of n to simulate more concurrent requests
	pthread_t tid[n];
	int deposit_ammount[n];

	//Fill the deposit_ammount array with random values between 1 to 10000
	for(i = 0; i < n; i++)
		deposit_ammount[i] = 1 + (int)(10000.0 * (rand()/(RAND_MAX + 1.0)));

	//n number of concurrent request to deposit money in account
	for(i = 0; i < n; i++)
		while(pthread_create(&tid[i], NULL, &deposit, (void*)&deposit_ammount[i])) {
			printf("Thread creation failed! Please try later!\n");
			sleep(1);
		}

	for(i = 0; i < n; i++)
		pthread_join(tid[i], NULL);
	
	printf("After the transactions end\n\nAccount Holder: %s, Update Balance: Rs. %d\n\n", yac.name, yac.balance);
	return 0;
}


#include <pthread.h>
#include <stdio.h>
#include <stdint.h>

void *function1(void *param);
void *function2(void *param);

volatile int sum;

int main(int argc, char *argv[]) {
	pthread_t tid1, tid2;
	pthread_attr_t attr;

	pthread_attr_init(&attr);
	pthread_create(&tid1, &attr, function1, (void *)10);
	pthread_create(&tid2, &attr, function2, (void *)10);

//	pthread_join(tid1, NULL);

	for (int i = 10; i > 0; --i) {
		if (i > 5) 
			sum += i;
		printf("Main thread counts: %d\n", i);
	}
	
	pthread_join(tid1,NULL);
	pthread_join(tid2, NULL);

	printf("Sum %d\n", sum);
	return 0;
}

void *function1(void *param) {
	int par = (int) param;
	for (int i = 1; i <= par; ++i){
		if (i < 6) sum += i;
		printf("Function 1 %d\n", i);
	}

	pthread_exit(0);
}
void *function2(void *param) {
	int par = (int) param;
	for (int i = 1; i <= par; i += 2) {
		sum += i;
		printf("Function 2 %d\n", i);
	}
	for (int i = 2; i <= par; i += 2)
		printf("Function 2 %d\n", i);

	pthread_exit(0);
}

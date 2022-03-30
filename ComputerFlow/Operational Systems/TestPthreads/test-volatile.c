#include <pthread.h>
#include <stdio.h>

volatile int sum;

void *fun(void *param) {
	sum += 10;
	return NULL;
}

int main(){
	pthread_t tid;
	pthread_attr_t attr;

	pthread_attr_init(&attr);
	pthread_create(&tid, &attr, fun, NULL);
	sum += 5;
	pthread_join(tid, NULL);
	printf("%d\n", sum);
	return 0;
}
	

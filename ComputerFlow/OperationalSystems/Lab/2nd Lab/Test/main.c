#include <stdio.h>
#include <stdlib.h>
int main(void) {
	int p, mypid;
	printf("The initial pid is %d\n", getpid());
	p = fork();
        p = fork();
	
	if (p < 0) {
		perror("fork");
		exit(1);
	}
	else if (p == 0) {
		mypid = getpid();
		printf("The child pid is %d\n", mypid);
	} else {
		mypid = getpid();
		printf("The father pid is %d\n", mypid);
	}
	return 0;
}

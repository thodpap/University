
#include "write_fun.h"


void  doWrite(int fd, char *  buff, int len){
        int idx = 0;
        idx = 0;
        int wcnt;
        do {
            wcnt = write(fd, buff + idx, len - idx);
            if(wcnt == -1){
                perror("write");
                exit(1);
            }
            else{
            idx += wcnt;
            }
        } while (idx < len);

}

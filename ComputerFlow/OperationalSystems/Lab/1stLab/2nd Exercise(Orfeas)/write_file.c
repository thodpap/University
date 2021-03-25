
#include "write_file.h"


void  write_file(int fd, const char *infile, int fd_inn, char* buff, bool boo){

        if(boo == true){
                doWrite(fd, buff, strlen(buff));

        }
        else{

                int fd1;
                fd1 = open(infile, O_RDONLY);


                if(fd1 == -1){
                        printf("%s: No such file or directory \n", infile);
                        exit(1);
                }

                FILE * fp = fdopen(fd1, "r");

                fseek(fp, 0L, SEEK_END);
                long int res = ftell(fp); // it affects fd1 too
        //      fseek(fp, 0L, SEEK_SET); it doesnt affect fd1

                fd1 = open(infile, O_RDONLY);

                char * con;
                con = (char *)calloc(res+1, sizeof(char));



                ssize_t rcnt1 = 0;

                for(;;){

                        rcnt1 = read(fd1, con, res);
                        if(rcnt1 == 0){
                                break;
                        }
      
                        if(rcnt1 == -1){
                                perror("read"); 
                                exit(1);
                        }
                        
                }               
    
                //con[res-1] = 0; without \n between the files 
    
                doWrite(fd, con, strlen(con));
                        
                if(close(fd1) == -1){
                        printf("error closing file %s", infile);
                        exit(1);
                }

                free(con);
                fclose(fp);
        }
}

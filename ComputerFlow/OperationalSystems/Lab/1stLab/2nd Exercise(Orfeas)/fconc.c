
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "write_file.h"
//i#include "write_fun.h"
#include <unistd.h>
#include <stdbool.h>

struct all{

        int fd;
        char* copy;
        bool boo;
};


int main(int argc, char **argv){

    if(argc>4){
        printf("Too many arguments");
        return 0;
    }

    struct all array[2];


    if(argc > 4 || argc < 3){
        fprintf(stderr, "You need to only add 2 or 3 arguments\n");

        return 0;
    }

    int oflags = O_CREAT | O_WRONLY | O_TRUNC;

    int mode = S_IRUSR | S_IWUSR;

    int fd3;
    int i;

    for(i = 0; i < argc-1; i++){
            //printf("comparing ready\n");
            //printf("comparing = %d\n", strcmp(argv[i+1], "fconc.out"));
            if(argc==4 && i == argc-1) break;
            if((*argv[i+1] == *argv[argc-1] && argc == 4) || (0==strcmp(argv[i+1], "fconc.out") && argc == 3)){
                array[i].boo = true;
                printf("Waring: %s is already passed as an argument and it will be overwritten, are you sure?\n", argv[argc-1]);
                printf("Press enter to continue or any other button and enter to do not");
                
                char c;
    
                scanf("%c",&c);

                if(c == 10){
                        continue;
                }
                else return 0;

        }
    }

    FILE* files[argc-2];
    int counter = 0;
    for(i = 0; i<2; i++){
        if(array[i].boo == true){
                printf("i am bored\n");
                counter = counter+1;
                array[i].fd = open(argv[i+1], O_RDONLY);
                if(array[i].fd == -1){
                printf("%s: No such file or directory \n", argv[i+1]);
                exit(1);
                }


                files[i] = fdopen(array[i].fd, "r");

                fseek(files[i], 0L, SEEK_END);
                long int res = ftell(files[i]); // it affects array[i].fd too
                //fseek(fp, 0L, SEEK_SET); it doesnt affect array[i].fd
                fclose(files[i]);

                array[i].fd = open(argv[i+1], O_RDONLY);

                array[i].copy = (char *)calloc(res+1, sizeof(char));

                ssize_t rcnt1 = 0;

                for(;;){
                        rcnt1 = read(array[i].fd, array[i].copy, res);
                        if(rcnt1 == 0){
                                 break;
                        }

                        if(rcnt1 == -1){
                                perror("read");
                                exit(1);
                         }

                }
                printf("this is the one: %s\n", array[i].copy);
        }
    }

   if(argc == 4) fd3 = open(argv[argc-1], oflags, mode);
   else fd3 = open("fconc.out", oflags, mode);




   for(i = 0; i<argc-1; i++){
        if(argc==4 && i == argc-2) break;
        write_file(fd3, argv[i+1], array[i].fd, array[i].copy, array[i].boo);
   }


//   printf("counter: %d\n", counter); 
     for(i = 0; i<counter; i++){
        if(0 == strcmp(array[i].copy, "")) continue;
        free(array[i].copy);
        //printf("hallo there\n");
   }
  
   return 0;
}

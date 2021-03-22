
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

    struct all array[argc-2];


    printf("Nubmer of arguments: %d \n", argc);
    if(argc > 4 || argc < 3){
        fprintf(stderr, "You need to only add 2 or 3 arguments\n");

        return 0;
    }

    int oflags = O_CREAT | O_WRONLY | O_TRUNC;

    int mode = S_IRUSR | S_IWUSR;

    int fd3;
    int i;

    for(i = 0; i < argc-2; i++){
        if(*argv[i+1] == *argv[argc-1]){
                array[i].boo = true;
                printf("Waring: %s is already passed as an argument and it will be overwritten, are you sure?\n", argv[i+1]);
                printf("Press enter to continue or any other button and enter to do not\n");

                char c;

                scanf("%c",&c);

                if(c == 10){
                        continue;
                }
               else return 0;

        }
    }

    FILE* files[argc-2];

    for(i = 0; i<2; i++){
        if(array[i].boo == true){
                printf("we go a true one\n");

                array[i].fd = open(argv[i+1], O_RDONLY);

                if(array[i].fd == -1){
                printf("%s: No such file or directory \n", argv[i+1]);
                exit(1);
                }


                files[i] = fdopen(array[i].fd, "r");

                fseek(files[i], 0L, SEEK_END);
                long int res = ftell(files[i]); // it affects fd1 too
                //fseek(fp, 0L, SEEK_SET); it doesnt affect fd1
                fclose(files[i]);

                array[i].fd = open(argv[i+1], O_RDONLY);
                printf("%d\n", array[i].fd);
                array[i].copy = (char *)calloc(res+1, sizeof(char));

                ssize_t rcnt1 = 0;

                for(;;){
                        printf("hallo there\n");
                        rcnt1 = read(array[i].fd, array[i].copy, res);
                        if(rcnt1 == 0){
                                 break;
                        }

                        if(rcnt1 == -1){
                                perror("read");
                                exit(1);
                         }

                }

        }
    }

   if(argc == 4) fd3 = open(argv[argc-1], oflags, mode);
   else fd3 = open("fconc.out", oflags, mode);

   printf("%d\n", fd3);

   for(i = 1; i<argc-1; i++){
        write_file(fd3, argv[i], array[i-1].fd, array[i-1].copy, array[i-1].boo);
   }



   for(i = 1; i<argc-2; i++){
        free(array[i].copy);
   }

   return 0;
}
/*
tHIS IS A TEST1.
THIS IS THE SECOND TEST.
THIS IS A TEST1
THIS IS A TETS1
*/
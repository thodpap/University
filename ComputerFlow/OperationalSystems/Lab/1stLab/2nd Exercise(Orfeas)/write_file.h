
#ifndef WRITE_FILE_H
#define WRITE_FILE_H
#include "write_fun.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void write_file(int fd, const char *infile, int fd_inn,  char* buff, bool boo);

#endif
 
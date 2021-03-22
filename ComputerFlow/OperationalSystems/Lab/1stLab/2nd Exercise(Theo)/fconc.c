#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define defaultOutput "fconc.out" 

int main(int argc, char **argv) {   
    FILE *inputFile1, *inputFile2;  
    FILE *outputFile;

    /* Check if number of arguments is correct, if not show message to standard error */
    if (argc != 3 && argc != 4) {
        fprintf(stderr, "Usage: ./fconc infile1 infile2 [outfile (default:fconc.out)]\n");
        return 0;
    }  
 
    /* Open the 2 input files */
    inputFile1 = fopen(argv[1],"r");
    if (inputFile1 == NULL) {
    	fprintf(stderr, "%s: No such file or directory\n", argv[1]);
    	exit(EXIT_FAILURE);
    }

    inputFile2 = fopen(argv[2], "r");
    if (inputFile1 == NULL) {
    	fclose(inputFile1);
    	fprintf(stderr, "%s: No such file or directory\n", argv[2]);
    	exit(EXIT_FAILURE);
    }
    
    /* Open the output file */ 
    if (argc == 4) { 
        if ((strcmp(argv[1], argv[3]) == 0) | (strcmp(argv[2], argv[3]) == 0) ) {
            outputFile = fopen(defaultOutput, "w+");      
        }
        else{
            outputFile = fopen(argv[3], "w+");
        }        
    } else { 
        outputFile = fopen(defaultOutput, "w+");  
    } 

    /* Read from files character by character and immediately 
        write to the output file (char by char)*/ 
    char ch;
    while((ch = fgetc(inputFile1)) != EOF) { 
        fputc(ch,outputFile);
    } 
 	
    while((ch = fgetc(inputFile2)) != EOF) {
        fputc(ch,outputFile);
    }

    fclose(inputFile1);
    fclose(inputFile2);
    fclose(outputFile);

    return 0;
}
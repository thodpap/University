/*
 * main.c
 *
 * Created: 5/16/2021 7:09:28 PM
 *  Author: Admin
 */ 
/* 
#include <xc.h>
#include <avr/io.h>

// AVR LAB EX 2
char A,B,C,D,F0,F1;

int main(void) { 
    DDRB = 0xFF; // B output
    DDRA = 0x00; // A input
    
    while(1)
    {  
        // PINA is the input
        // PORTB is the output
        // we want it like ****DCBA 
        A = PINA & 0x01;
        B = PINA & 0x02;
        C = PINA & 0x04;
        D = PINA & 0x08;

        // F0 = (ABC' + CD)' 
        // F1= (A+B)*(C+D)
        F0 = !( (A & B & !(C & 0x01)) | (C & D));
        F1 = (A|B)&(C|D) << 1;
        PORTB = F1 | F0;
    }
} */


/* 
// This is last years ex 2 (exams)
#include <avr/io.h>
// #include <mega16.h> 

char A0,A1,A2,A3,A4,A5,A6,A7;
char input;
char F; 

interrupt [EXT_INT1] void ext_int0_isr(void){
    PORTC = F & 0x00; // reset 
}

int main() {
    DDRC = 0xFF; // initialize PORTC to output
    DDRA = 0x00; // initialize PORTA to input

    while (1) { 
        input = PINA;
        A0 = input & 0x01;
        A1 = input & 0x02 >> 1;
        A2 = input & 0x04 >> 2;
        A3 = input & 0x08 >> 3;
        A4 = input & 0x16 >> 4;
        A5 = input & 0x32 >> 5;
        A6 = input & 0x64 >> 6;
        A7 = input & 0x128 >> 7;

        F = ((A0 & A1) | (A2 & A3) | (A4 ^ A5) | (A6 ^ A7)) << 2;
        PORTC = F;
    }
} */

#include <avr/io.h>
#include <mega16.h> 

char A1,A0;
char K1,K0;
char W;
char input;
char output; 

void init() {
    while (1) {
        input = PIND; // read input
        input = PIND; // read input
        A1 = input & 0x01; // Get A1 digit
        K1 = input & 0x02 >> 1; // Get K1 digit
        A0 = input & 0x04 >> 2; // Get A0 digit
        K0 = input & 0x08 >> 3; // Get K1 digit
        W  = input & 0x16 >> 4; // Get W digit
        if (A1 == 1) {
            output = 0x01; // steile sto isogio
        } else {
            output = 0x00;
            break;
        }
    }
}
int main() {
    DDRD = 0x00; // set D as input
    DDRB = 0xFF; // set B as output 
    
    init();

    while (1) {
        input = PIND; // read input
        A1 = input & 0x01; // Get A1 digit
        K1 = input & 0x02 >> 1; // Get K1 digit
        A0 = input & 0x04 >> 2; // Get A0 digit
        K0 = input & 0x08 >> 3; // Get K1 digit
        W  = input & 0x16 >> 4; // Get W digit
        if ( (A1 == 1 && A0 == 1) | (A1 == 0 && A0 == 0) ) { 
            output = 0x03; // 11 as output indicates error
        }
        else if (A1 == 1) {
            if (W == 1 || K0 == 1) {
                output = 0x01;
            } else {
                output = 0x00;
            }
        } else if (A0 == 1) {
            if (W == 1 || K0 == 1) {
                output = 0x02;
            } else {
                output = 0x00;
            }
        }    
        PORTB = output; 
    }
}
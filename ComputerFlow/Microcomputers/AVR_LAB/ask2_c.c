/*
 * main.c
 *
 * Created: 5/16/2021 7:09:28 PM
 *  Author: Admin
 */ 

#include <xc.h>
#include <avr/io.h>

//initializations
char A;
char B;
char C;
char D;
char temp;
char F0;
char F1;

int main(void) 
{ // add breakpoint here
	DDRB = 0xFF;
	DDRA = 0x00;
	
    while(1)
    {
        A = PINA & 0x01;
	temp = PINA >> 1;
	B = temp & 0x01;
	temp = temp >> 1;
	C = temp & 0x01;
	temp = temp >> 1;
	D = temp & 0x01;
		
	F0 = !(A & B & (!C & 0x01) | C & D);
	F1 = (A | B) & (C | D);
		
	F1 = F1 << 1;
	PORTB = F1 | F0;
		
    }
}

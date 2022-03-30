/*
 * ask1_c.c
 *
 * Created: 11/2/2021 6:23:46 PM
 * Author : thodpap
 */ 
/*
 * ask1_c.c
 *
 * Created: 11/1/2021 8:20:10 PM
 * Author : thodpap
 */ 

#include <avr/io.h>

char A,B,C,D;
char F0;
char F1;

int main(void)
{
	DDRC = 0x00; // C is input
	DDRB = 0xff; // B is output
	
	
    /* Replace with your application code */
    while (1) 
    {
		char input = PINC;
		A = (input & 0x01);
		B = (input & 0x02) >> 1;
		C = (input & 0x04) >> 2;
		D = (input & 0x08) >> 3;
		
		F0 = !( ((!A) & B) | ((!B) & C & D) );
		F1 = (A & C) | (B | D);
		F1 = F1 << 1;
		PORTB = F1 | F0;	
		
    }
}


